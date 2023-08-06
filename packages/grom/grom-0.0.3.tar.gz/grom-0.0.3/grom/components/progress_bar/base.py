"""
Progress bar implementation on top of prompt_toolkit.

::

    with GromProgressBar(...) as pb:
        for item in pb(data):
            ...
"""
import datetime
import functools
import os
import signal
import threading
import traceback
from asyncio import new_event_loop, set_event_loop
from typing import Callable, Generic, Iterable, Iterator, List, Optional, Sequence, Sized, TypeVar, cast

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app_session
from prompt_toolkit.formatted_text import AnyFormattedText, StyleAndTextTuples, to_formatted_text
from prompt_toolkit.input import Input
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout import HSplit, Layout, VSplit, Window
from prompt_toolkit.layout.controls import UIContent, UIControl
from prompt_toolkit.layout.dimension import AnyDimension, D
from prompt_toolkit.output import Output

try:
    import contextvars
except ImportError:
    from prompt_toolkit.eventloop import dummy_contextvars
    contextvars = dummy_contextvars  # type: ignore

from grom.containers import bottom_toolbar_container, margin_container, title_container
from grom.theme import GromThemer

from .formatters import Formatter, create_default_formatters

__all__ = ["GromProgressBar"]

E = KeyPressEvent

_SIGWINCH = getattr(signal, "SIGWINCH", None)


def create_key_bindings(cancel_callback: Optional[Callable[[], None]]) -> KeyBindings:
    """
    Key bindings handled by the progress bar.
    (The main thread is not supposed to handle any key bindings.)
    """
    key_bindings = KeyBindings()

    @key_bindings.add("escape")
    def _esc(_: E) -> None:
        os.kill(os.getpid(), signal.SIGINT)

    @key_bindings.add("c-l")
    def _clear(event: E) -> None:
        event.app.renderer.clear()

    if cancel_callback is not None:

        @key_bindings.add("c-c")
        def _interrupt(_: E) -> None:
            "Kill the 'body' of the progress bar, but only if we run from the main thread."
            cancel_callback()

    return key_bindings


_T = TypeVar("_T")


class GromProgressBar:
    """
    Progress bar context manager.

    Usage ::

        with GromProgressBar(...) as pb:
            for item in pb(data):
                ...

    :param title: Text to be displayed above the progress bars. This can be a
        callable or formatted text as well.
    :param formatters: List of :class:`.Formatter` instances.
    :param bottom_toolbar: Text to be displayed in the bottom toolbar. This
        can be a callable or formatted text.
    :param key_bindings: :class:`.KeyBindings` instance.
    :param cancel_callback: Callback function that's called when control-c is
        pressed by the user. This can be used for instance to start "proper"
        cancellation if the wrapped code supports it.
    :param output: :class:`~prompt_toolkit.output.Output` instance.
    :param input: :class:`~prompt_toolkit.input.Input` instance.
    :param erase_when_done: Set if progress bar should be deleted when finished, or not.
    """

    def __init__(
        self,
        title: AnyFormattedText = None,
        formatters: Optional[Sequence[Formatter['GromProgressBar', 'ProgressBarCounter']]] = None,
        bottom_toolbar: AnyFormattedText = None,
        key_bindings: Optional[KeyBindings] = None,
        cancel_callback: Optional[Callable[[], None]] = None,
        output: Optional[Output] = None,
        input: Optional[Input] = None,  # pylint: disable=redefined-builtin
        erase_when_done: bool = False
    ) -> None:
        self.app = None
        self.title = title
        self.formatters = formatters or create_default_formatters()
        self.bottom_toolbar = bottom_toolbar
        self.counters: List[ProgressBarCounter[object]] = []
        self.key_bindings = key_bindings
        self.cancel_callback = cancel_callback
        self.erase_when_done = erase_when_done

        # If no `cancel_callback` was given, and we're creating the progress
        # bar from the main thread. Cancel by sending a `KeyboardInterrupt` to
        # the main thread.
        if (
            self.cancel_callback is None and
            threading.currentThread() == threading.main_thread()  # pylint: disable=W4902
        ):

            def keyboard_interrupt_to_main_thread() -> None:
                os.kill(os.getpid(), signal.SIGINT)

            self.cancel_callback = keyboard_interrupt_to_main_thread

        # Note that we use __stderr__ as default error output, because that
        # works best with `patch_stdout`.
        self.output = output or get_app_session().output
        self.input = input or get_app_session().input

        self._thread: Optional[threading.Thread] = None

        self._app_loop = new_event_loop()
        self._has_sigwinch = False
        self._app_started = threading.Event()

    def __enter__(self) -> "GromProgressBar":
        # Create UI Application.
        def width_for_formatter(formatter: Formatter['GromProgressBar', 'ProgressBarCounter']) -> AnyDimension:
            # Needs to be passed as callable (partial) to the 'width'
            # parameter, because we want to call it on every resize.
            return formatter.get_width(component=self)

        progress_controls = [
            Window(
                content=_ProgressControl(self, f, self.cancel_callback),
                width=functools.partial(width_for_formatter, f),
            )
            for f in self.formatters
        ]

        self.app: Application[None] = Application(
            min_redraw_interval=0.05,
            erase_when_done=self.erase_when_done,
            full_screen=False,
            layout=Layout(
                HSplit(
                    [
                        margin_container(),
                        title_container(self.title),
                        VSplit(
                            progress_controls,
                            height=lambda: D(
                                preferred=len(self.counters), max=len(self.counters)
                            ),
                        ),
                        Window(),
                        margin_container(),
                        bottom_toolbar_container(self.bottom_toolbar),
                    ]
                )
            ),
            style=GromThemer().style,
            key_bindings=self.key_bindings,
            refresh_interval=0.2,
            color_depth=GromThemer().theme.color_depth,
            output=self.output,
            input=self.input,
        )

        # Run application in different thread.
        def run() -> None:
            set_event_loop(self._app_loop)
            try:
                self.app.run(pre_run=self._app_started.set)
            except BaseException as e:  # pylint: disable=broad-except
                traceback.print_exc()
                print(e)

        ctx: contextvars.Context = contextvars.copy_context()

        self._thread = threading.Thread(target=ctx.run, args=(run,))
        self._thread.start()

        return self

    def __exit__(self, *a: object) -> None:
        # Wait for the app to be started. Make sure we don't quit earlier,
        # otherwise `self.app.exit` won't terminate the app because
        # `self.app.future` has not yet been set.
        self._app_started.wait()

        # Quit UI application.
        if self.app.is_running:
            self._app_loop.call_soon_threadsafe(self.app.exit)

        if self._thread is not None:
            self._thread.join()
        self._app_loop.close()

    def __call__(
        self,
        data: Optional[Iterable[_T]] = None,
        label: AnyFormattedText = "",
        remove_when_done: bool = False,
        total: Optional[int] = None,
    ) -> "ProgressBarCounter[_T]":
        """
        Start a new counter.

        :param label: Title text or description for this progress. (This can be
            formatted text as well).
        :param remove_when_done: When `True`, hide this progress bar.
        :param total: Specify the maximum value if it can't be calculated by
            calling ``len``.
        """
        counter = ProgressBarCounter(
            self, data, label=label, remove_when_done=remove_when_done, total=total
        )
        self.counters.append(counter)
        return counter

    def invalidate(self) -> None:
        self.app.invalidate()


class _ProgressControl(UIControl):
    """
    User control for the progress bar.
    """

    def __init__(
        self,
        progress_bar: GromProgressBar,
        formatter: Formatter['GromProgressBar', 'ProgressBarCounter'],
        cancel_callback: Optional[Callable[[], None]],
    ) -> None:
        self.progress_bar = progress_bar
        self.formatter = formatter
        self._key_bindings = create_key_bindings(cancel_callback)

    def create_content(self, width: int, height: int) -> UIContent:
        items: List[StyleAndTextTuples] = []

        for progress_counter in self.progress_bar.counters:
            try:
                text = self.formatter.format(self.progress_bar, progress_counter, width)
            except BaseException:  # pylint: disable=broad-except
                traceback.print_exc()
                text = "ERROR"

            items.append(to_formatted_text(text))

        def get_line(i: int) -> StyleAndTextTuples:
            return items[i]

        return UIContent(get_line=get_line, line_count=len(items), show_cursor=False)

    def is_focusable(self) -> bool:
        return True  # Make sure that the key bindings work.

    def get_key_bindings(self) -> KeyBindings:
        return self._key_bindings


_CounterItem_co = TypeVar("_CounterItem_co", covariant=True)


class ProgressBarCounter(Generic[_CounterItem_co]):
    """
    An individual counter (A progress bar can have multiple counters).
    """

    def __init__(
        self,
        progress_bar: GromProgressBar,
        data: Optional[Iterable[_CounterItem_co]] = None,
        label: AnyFormattedText = "",
        remove_when_done: bool = False,
        total: Optional[int] = None,
    ) -> None:

        self.start_time = datetime.datetime.now()
        self.stop_time: Optional[datetime.datetime] = None
        self.progress_bar = progress_bar
        self.data = data
        self.items_completed = 0
        self.label = label
        self.remove_when_done = remove_when_done
        self._done = False
        self.total: Optional[int]

        if total is None:
            try:
                self.total = len(cast(Sized, data))
            except TypeError:
                self.total = None  # We don't know the total length.
        else:
            self.total = total

    def __iter__(self) -> Iterator[_CounterItem_co]:
        if self.data is not None:
            try:
                for item in self.data:
                    yield item
                    self.item_completed()

                # Only done if we iterate to the very end.
                self.done = True
            finally:
                # Ensure counter has stopped even if we did not iterate to the
                # end (e.g. break or exceptions).
                self.stopped = True
        else:
            raise NotImplementedError("No data defined to iterate over.")

    def item_completed(self) -> None:
        """
        Start handling the next item.

        (Can be called manually in case we don't have a collection to loop through.)
        """
        self.items_completed += 1
        self.progress_bar.invalidate()

    @property
    def done(self) -> bool:
        """Whether a counter has been completed.

        Done counter have been stopped (see stopped) and removed depending on
        remove_when_done value.

        Contrast this with stopped. A stopped counter may be terminated before
        100% completion. A done counter has reached its 100% completion.
        """
        return self._done

    @done.setter
    def done(self, value: bool) -> None:
        self._done = value
        self.stopped = value

        if value and self.remove_when_done:
            self.progress_bar.counters.remove(self)

    @property
    def stopped(self) -> bool:
        """Whether a counter has been stopped.

        Stopped counters no longer have increasing time_elapsed. This distinction is
        also used to prevent the Bar formatter with unknown totals from continuing to run.

        A stopped counter (but not done) can be used to signal that a given counter has
        encountered an error but allows other counters to continue
        (e.g. download X of Y failed). Given how only done counters are removed
        (see remove_when_done) this can help aggregate failures from a large number of
        successes.

        Contrast this with done. A done counter has reached its 100% completion.
        A stopped counter may be terminated before 100% completion.
        """
        return self.stop_time is not None

    @stopped.setter
    def stopped(self, value: bool) -> None:
        if value:
            # This counter has not already been stopped.
            if not self.stop_time:
                self.stop_time = datetime.datetime.now()
        else:
            # Clearing any previously set stop_time.
            self.stop_time = None

    @property
    def percentage(self) -> float:
        if self.total is None:
            return 0
        return self.items_completed * 100 / max(self.total, 1)

    @property
    def time_elapsed(self) -> datetime.timedelta:
        """
        Return how much time has been elapsed since the start.
        """
        if self.stop_time is None:
            return datetime.datetime.now() - self.start_time
        return self.stop_time - self.start_time

    @property
    def time_left(self) -> Optional[datetime.timedelta]:
        """
        Timedelta representing the time left.
        """
        if self.total is None or not self.percentage:
            return None
        if self.done or self.stopped:
            return datetime.timedelta(0)
        return self.time_elapsed * (100 - self.percentage) / self.percentage
