"""
Text Formatter
"""
from typing import TYPE_CHECKING

from prompt_toolkit.formatted_text import (
    AnyFormattedText,
    to_formatted_text,
)
from prompt_toolkit.formatted_text.utils import fragment_list_width
from prompt_toolkit.layout.dimension import AnyDimension

from .format import Formatter

if TYPE_CHECKING:
    from .format import T, V


class Text(Formatter["T", "V"]):
    """
    Display plain text.
    """

    def __init__(self, text: AnyFormattedText, style: str = "") -> None:
        self.text = to_formatted_text(text, style=style)

    def format(
        self,
        component: "T",
        child: "V[object]",
        width: int,
    ) -> AnyFormattedText:
        return self.text

    def get_width(self, component: "T") -> AnyDimension:
        return fragment_list_width(self.text)
