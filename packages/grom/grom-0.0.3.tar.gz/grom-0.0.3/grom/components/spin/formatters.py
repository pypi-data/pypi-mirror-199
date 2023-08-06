"""
GromFormatter classes for the Grom child.
Each spinner consists of a list of these formatters.
"""
import datetime
from typing import TYPE_CHECKING, List

from prompt_toolkit.formatted_text import (
    HTML,
    AnyFormattedText
)
from prompt_toolkit.layout.dimension import AnyDimension
from grom.formatters import Formatter, Text, Label, Filler, Spinner
from grom.theme import GromThemer

if TYPE_CHECKING:
    from .base import GromSpinner, GromSpinnerCounter

__all__ = [
    "SpinTimeElapsed",
    "create_default_spin_formatters",
]


def _format_timedelta(timedelta: datetime.timedelta) -> str:
    """
    Return hh:mm:ss, or mm:ss if the amount of hours is zero.
    """
    result = f"{timedelta}".split(".")[0]
    if result.startswith("0:"):
        result = result[2:]
    return result


class SpinTimeElapsed(Formatter['GromSpinner', 'GromSpinnerCounter']):
    """
    Display the elapsed time.
    """

    def format(
        self,
        component: "GromSpinner",
        child: "GromSpinnerCounter[object]",
        width: int,
    ) -> AnyFormattedText:

        text = _format_timedelta(child.time_elapsed).rjust(width)
        return HTML("<time-elapsed>{time_elapsed}</time-elapsed>").format(
            time_elapsed=text
        )

    def get_width(self, component: "GromSpinner") -> AnyDimension:
        all_values = [
            len(_format_timedelta(c.time_elapsed)) for c in component.counters
        ]
        if all_values:
            return max(all_values)
        return 0


def create_default_spin_formatters() -> List[Formatter]:
    """
    Return the list of default formatters.
    """
    return [
        Text(" " * GromThemer().theme.margin_vertical),
        Spinner(),
        Text("  "),
        Label(),
        Filler(),
        SpinTimeElapsed(),
        Text(" " * GromThemer().theme.margin_vertical),
    ]
