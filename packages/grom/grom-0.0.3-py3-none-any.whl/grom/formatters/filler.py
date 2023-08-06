"""
Filler Formatter
"""
import os
from typing import TYPE_CHECKING

from prompt_toolkit.formatted_text import (
    AnyFormattedText,
)

from prompt_toolkit.layout.dimension import AnyDimension, D

from .format import Formatter

if TYPE_CHECKING:
    from .format import T, V


class Filler(Formatter['T', 'V']):
    """
    Fill space, pushing other formatters to the right.
    """

    def __init__(self) -> None:
        pass

    def format(
        self,
        component: 'T',
        child: 'V[object]',
        width: int,
    ) -> AnyFormattedText:
        return " " * os.get_terminal_size().columns

    def get_width(self, component: 'T') -> AnyDimension:
        return D(min=5)
