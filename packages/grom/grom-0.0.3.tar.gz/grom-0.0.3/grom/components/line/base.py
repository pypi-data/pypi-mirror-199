"""
Grom - Frame
"""
from functools import partial
from typing import Type

from prompt_toolkit.formatted_text import AnyFormattedText, Template
from prompt_toolkit.layout import Window
from prompt_toolkit.layout.containers import Container, VSplit
from prompt_toolkit.shortcuts import print_container
from prompt_toolkit.widgets import Label

from grom.theme import GromThemer


class _Line:  # pylint: disable=R0913,R0902,R0903
    def __init__(
        self,
        line_char: chr,
        title: AnyFormattedText = "",
        style: str = "",
        margin: tuple[int] = (0, 0),
        width: int = None,
    ) -> None:

        self._title = title
        self._line_char = line_char
        self._style = style
        self._margin = margin
        self._width = width
        self._fill = partial(Window, style="class:frame.border")

        style = "class:frame " + self._style

        self.container = VSplit([
            VSplit(
                self._append_margin([
                    self._fill(char=self._line_char),
                    Label(
                        lambda: Template(" {} ").format(self._title),
                        style="class:frame.title",
                        dont_extend_width=True,
                    ),
                    self._fill(char=self._line_char),
                ]),
                height=1,
                width=self._width
            )
        ], width=self._width)

    def _append_margin(self, arr):
        if self._margin[1] > 0:
            arr.insert(0, self._fill(width=self._margin[1], height=1, char=" "))
            arr.append(self._fill(width=self._margin[1], height=1, char=" "))
        return arr

    def __pt_container__(self) -> Container:
        return self.container


def grom_line(
        title: AnyFormattedText | Type[None] = None,
        line_char: chr = '─',
        width: int = None,
        margin: tuple[int] = None,
):

    if margin is None or len(margin) < 2:
        margin = (0, 0)

    print_container(
        _Line(
            title=title,
            width=width,
            margin=margin,
            line_char=line_char
        ),
        style=GromThemer().style
    )


if __name__ == '__main__':
    grom_line('foo')
