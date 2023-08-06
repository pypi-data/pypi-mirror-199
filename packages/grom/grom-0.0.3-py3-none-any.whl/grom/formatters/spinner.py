"""
Spinner Formatter

Requires the properties done and stopped on the child object (V).
"""
import time
from typing import TYPE_CHECKING

from prompt_toolkit.formatted_text import AnyFormattedText, HTML
from prompt_toolkit.layout.dimension import AnyDimension, D
from prompt_toolkit.utils import get_cwidth
from grom.theme import GromSpinnerStyle, spinner_style_from_arg
from .format import Formatter

if TYPE_CHECKING:
    from .format import T, V


class Spinner(Formatter["T", "V"]):
    """
    Display a spinning wheel.
    """

    def __init__(
        self,
        spinner_style: GromSpinnerStyle = None,
        show_done: bool = True,
        show_stopped: bool = True,
    ) -> None:
        self.spinner_style = spinner_style_from_arg(spinner_style)
        self._show_done = show_done
        self._show_stopped = show_stopped
        self._space = (
            " "
            if get_cwidth(self.spinner_style.frames[0]) > len(self.spinner_style.frames[0])
            else ""
        )
        self._completed = self.spinner_style.done_frame

    # pylint: disable=unused-argument
    def format(
        self,
        component: "T",
        child: "V[object]",
        width: int,
    ) -> AnyFormattedText:
        index = int(time.time() * self.spinner_style.fps) % len(
            self.spinner_style.frames
        )
        output = self.spinner_style.frames[index]
        if child.done and self._show_done:
            output = self.spinner_style.done_frame
        elif child.stopped and self._show_stopped:
            output = self.spinner_style.stopped_frame
        return HTML(f"<spinning-wheel>{output}{self._space}</spinning-wheel>")

    def get_width(self, component: "T") -> AnyDimension:
        return D.exact(len(self.spinner_style.frames[0]) + len(self._space))
