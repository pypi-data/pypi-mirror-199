"""
Style borders
"""
from enum import Enum
from dataclasses import dataclass


@dataclass
class BorderChars:  # pylint: disable=R0902
    """Border frame chars"""
    top: chr
    bottom: chr
    left: chr
    right: chr
    top_left: chr
    top_right: chr
    bottom_left: chr
    bottom_right: chr
    title_left: chr
    title_right: chr


class Border(Enum):
    """Border enum containing all the fram border variants"""
    SLIM = BorderChars("─", "─", "│", "│", "┌", "┐", "└", "┘", "┤", "├")
    ROUNDED = BorderChars("─", "─", "│", "│", "╭", "╮", "╰", "╯", "─", "─")
    BLOCK = BorderChars("█", "█", "█", "█", "█", "█", "█", "█", None, None)
    OUTERHALF = BorderChars("▀", "▄", "▌", "▐", "▛", "▜", "▙", "▟", None, None)
    INNERHALF = BorderChars("▄", "▀", "▐", "▌", "▗", "▖", "▝", "▘", None, None)
    THICK = BorderChars("━", "━", "┃", "┃", "┏", "┓", "┗", "┛", "┫", "┣")
    DOUBLE = BorderChars("═", "═", "║", "║", "╔", "╗", "╚", "╝", "╣", "╠")
    HIDDEN = BorderChars(" ", " ", " ", " ", " ", " ", " ", " ", " ", " ")

    def __str__(self):
        return self.name.lower()


def border_from_source(s: str | BorderChars) -> BorderChars:
    if s is None:
        return Border.THICK.value
    if isinstance(s, BorderChars):
        return s
    for data in Border:
        if data.name.casefold() == s.casefold():
            return data.value
    raise NotImplementedError("Unsupported border name")
