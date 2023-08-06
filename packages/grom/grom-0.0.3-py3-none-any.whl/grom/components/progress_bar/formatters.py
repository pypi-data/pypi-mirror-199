"""
Formatter classes for the progress bar.
Each progress bar consists of a list of these formatters.
"""
import datetime
import time

from typing import TYPE_CHECKING, List

from prompt_toolkit.formatted_text import HTML, AnyFormattedText
from prompt_toolkit.layout.dimension import AnyDimension, D
from prompt_toolkit.utils import get_cwidth

from grom.theme import GromThemer
from grom.tools.colors import RGB, gradient
from grom.formatters import Formatter, Text, Label


if TYPE_CHECKING:
    from .base import GromProgressBar, ProgressBarCounter


__all__ = [
    "Percentage",
    "Progress",
    "TimeElapsed",
    "TimeLeft",
    "IterationsPerSecond",
    "GradientBar",
    "create_default_formatters",
]


class Percentage(Formatter["GromProgressBar", "ProgressBarCounter"]):
    """
    Display the progress as a percentage.
    """

    template = "<percentage>{percentage:>5}%</percentage>"

    def format(
        self,
        component: "GromProgressBar",
        child: "ProgressBarCounter[object]",
        width: int,
    ) -> AnyFormattedText:

        return HTML(self.template).format(percentage=round(child.percentage, 1))

    def get_width(self, component: "GromProgressBar") -> AnyDimension:
        return D.exact(6)


class Progress(Formatter["GromProgressBar", "ProgressBarCounter"]):
    """
    Display the progress as text.  E.g. "8/20"
    """

    template = "<current>{current:>3}</current>/<total>{total:>3}</total>"

    def format(
        self,
        component: "GromProgressBar",
        child: "ProgressBarCounter[object]",
        width: int,
    ) -> AnyFormattedText:

        return HTML(self.template).format(
            current=child.items_completed, total=child.total or "?"
        )

    def get_width(self, component: "GromProgressBar") -> AnyDimension:
        all_lengths = [len("{:>3}".format(c.total or "?")) for c in component.counters]
        all_lengths.append(1)
        return D.exact(max(all_lengths) * 2 + 1)


def _format_timedelta(timedelta: datetime.timedelta) -> str:
    """
    Return hh:mm:ss, or mm:ss if the amount of hours is zero.
    """
    result = f"{timedelta}".split(".")[0]
    if result.startswith("0:"):
        result = result[2:]
    return result


class TimeElapsed(Formatter["GromProgressBar", "ProgressBarCounter"]):
    """
    Display the elapsed time.
    """

    def format(
        self,
        component: "GromProgressBar",
        child: "ProgressBarCounter[object]",
        width: int,
    ) -> AnyFormattedText:

        text = _format_timedelta(child.time_elapsed).rjust(width)
        return HTML("<time-elapsed>{time_elapsed}</time-elapsed>").format(
            time_elapsed=text
        )

    def get_width(self, component: "GromProgressBar") -> AnyDimension:
        all_values = [
            len(_format_timedelta(c.time_elapsed)) for c in component.counters
        ]
        if all_values:
            return max(all_values)
        return 0


class TimeLeft(Formatter["GromProgressBar", "ProgressBarCounter"]):
    """
    Display the time left.
    """

    template = "<time-left>{time_left}</time-left>"
    unknown = "?:??:??"

    def format(
        self,
        component: "GromProgressBar",
        child: "ProgressBarCounter[object]",
        width: int,
    ) -> AnyFormattedText:

        time_left = child.time_left
        if time_left is not None:
            formatted_time_left = _format_timedelta(time_left)
        else:
            formatted_time_left = self.unknown

        return HTML(self.template).format(time_left=formatted_time_left.rjust(width))

    def get_width(self, component: "GromProgressBar") -> AnyDimension:
        all_values = [
            len(_format_timedelta(c.time_left)) if c.time_left is not None else 7
            for c in component.counters
        ]
        if all_values:
            return max(all_values)
        return 0


class IterationsPerSecond(Formatter["GromProgressBar", "ProgressBarCounter"]):
    """
    Display the iterations per second.
    """

    template = (
        "<iterations-per-second>{iterations_per_second:.2f}</iterations-per-second>"
    )

    def format(
        self,
        component: "GromProgressBar",
        child: "ProgressBarCounter[object]",
        width: int,
    ) -> AnyFormattedText:

        value = child.items_completed / child.time_elapsed.total_seconds()
        return HTML(self.template.format(iterations_per_second=value))

    def get_width(self, component: "GromProgressBar") -> AnyDimension:
        all_values = [
            len(f"{c.items_completed / c.time_elapsed.total_seconds():.2f}")
            for c in component.counters
        ]
        if all_values:
            return max(all_values)
        return 0


class GradientBar(Formatter["GromProgressBar", "ProgressBarCounter"]):
    """
    Display a gradient progress bar.
    """

    def __init__(
        self,
        start: str = "",
        end: str = "",
        sym_fg: str = "▇",
        sym_bg: str = "░",
        sym_unknown: str = "▇",
        theme: GromThemer = None,
    ) -> None:

        assert len(sym_fg) == 1 and get_cwidth(sym_fg) == 1
        assert len(sym_bg) == 1 and get_cwidth(sym_bg) == 1

        self.start = start
        self.end = end
        self.sym_fg = sym_fg
        self.sym_bg = sym_bg
        self.sym_unknown = sym_unknown
        self.gradient_colors: list(RGB) = None
        self.bar_width = None
        self.theme = GromThemer().theme if theme is None else theme

    def format(
        self,
        component: "GromProgressBar",
        child: "ProgressBarCounter[object]",
        width: int,
    ) -> AnyFormattedText:
        if self.get_width(component) != self.bar_width:
            self.gradient_colors = gradient(
                self.theme.colors.gradient_start, self.theme.colors.gradient_end, width
            )

        if child.done or child.total or child.stopped:
            percent = 1.0 if child.done else child.percentage / 100
        else:
            percent = time.time() * 20 % 100 / 100

        width -= get_cwidth(self.start + self.end)
        pb_fg = int(percent * width)

        if child.done or child.total or child.stopped:
            bar_bg = self.sym_bg * (width - pb_fg)
            template = f"<progressbar>{self.start}[HOLDER]<progressbar-bg>{bar_bg}</progressbar-bg>{self.end}</progressbar>"

            str_list = []
            for a in range(pb_fg):
                str_list.append(
                    f'<bar-fg fg="{self.gradient_colors[a].to_hex()}">{self.sym_fg}</bar-fg>'
                )

            template = template.replace("[HOLDER]", "".join(str_list))
        else:
            bar_bg1 = self.sym_bg * (pb_fg)
            bar_bg2 = self.sym_bg * (width - pb_fg - 1)
            unknown = self.sym_unknown
            unknown_color = self.gradient_colors[pb_fg].to_hex()
            template = (
                f'<progressbar>{self.start}<progressbar-bg>{bar_bg1}</progressbar-bg>'
                f'<progress-unknown fg="{unknown_color}">{unknown}</progress-unknown>'
                f'<progressbar-bg>{bar_bg2}</progressbar-bg>{self.end}</progressbar>'
            )

        return HTML(template)

    def get_width(self, component: "GromProgressBar") -> AnyDimension:
        return D(min=9)


def create_default_formatters() -> List[Formatter]:
    """
    Return the list of default formatters.
    """
    return [
        Text(" " * GromThemer().theme.margin_vertical),
        Label(),
        Text("  "),
        GradientBar(),
        Text("  "),
        Percentage(),
        Text(" " * GromThemer().theme.margin_vertical),
    ]
