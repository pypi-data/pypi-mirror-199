"""
Grom - Frame
"""
from functools import partial
from typing import Type


from prompt_toolkit.formatted_text import AnyFormattedText, Template
from prompt_toolkit.layout import Window, WindowAlign
from prompt_toolkit.layout.containers import AnyContainer, Container, DynamicContainer, HSplit, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl, UIControl
from prompt_toolkit.shortcuts import print_container
from prompt_toolkit.widgets import Label
from prompt_toolkit import HTML

from grom.theme import GromThemer

from .borders import BorderChars, border_from_source


class _Frame:  # pylint: disable=R0913,R0902,R0903
    def __init__(
        self,
        body: AnyContainer,
        border: BorderChars,
        title: AnyFormattedText = "",
        show_border: bool = True,
        style: str = "",
        margin: tuple[int] = (0, 0),
        padding: tuple[int] = (0, 0),
        width: int = None,
        height: int = None
    ) -> None:

        self._body = body
        self._title = title
        self._border = border
        self._show_border = show_border
        self._style = style
        self._margin = margin
        self._width = width
        self._height = height
        self._padding = padding
        self._fill = partial(Window, style="class:frame.border")
        self._left_width = 1 if self._border.title_left and len(self._border.title_left) > 0 else 0
        self._right_width = 1 if self._border.title_right and len(self._border.title_right) > 0 else 0

        style = "class:frame " + self._style
        self.container = HSplit(
            self._create_container_arr(),
            height=height,
            style=style
        )

    def _append_margin(self, arr):
        if self._margin[1] > 0:
            arr.insert(0, self._fill(width=self._margin[1], height=1, char=" "))
            arr.append(self._fill(width=self._margin[1], height=1, char=" "))
        return arr

    def _create_top_row(self):
        if bool(self._title):
            return VSplit([
                VSplit(
                    self._append_margin([
                        self._fill(width=1, height=1, char=self._border.top_left),
                        self._fill(char=self._border.top),
                        self._fill(width=self._left_width, height=1, char=self._border.title_left),
                        Label(
                            lambda: Template(" {} ").format(self._title),
                            style="class:frame.title",
                            dont_extend_width=True,
                        ),
                        self._fill(width=self._right_width, height=1, char=self._border.title_right),
                        self._fill(char=self._border.top),
                        self._fill(width=1, height=1, char=self._border.top_right),
                    ]),
                    height=1,
                    width=self._width
                )
            ], width=self._width)
        return VSplit(
            [
                VSplit(
                    self._append_margin([
                        self._fill(width=1, height=1, char=self._border.top_left),
                        self._fill(char=self._border.top),
                        self._fill(width=1, height=1, char=self._border.top_right),
                    ]),
                    height=1,
                    width=self._width
                )
            ],
            width=self._width
        )

    def _create_bottom_row(self):
        return VSplit([
            VSplit(
                self._append_margin([
                    self._fill(width=1, height=1, char=self._border.bottom_left),
                    self._fill(char=self._border.bottom),
                    self._fill(width=1, height=1, char=self._border.bottom_right),
                ]),
                height=1,
                width=self._width
            )],
            width=self._width

        )

    def _create_main_container(self):
        cnt = None
        if self._show_border:
            cnt = VSplit(
                self._append_margin([
                    VSplit(
                        [
                            self._fill(width=1, height=1, char=self._border.left),
                            DynamicContainer(lambda: self._body),
                            self._fill(width=1, char=self._border.right),
                        ],
                        padding=self._padding[1]
                    )
                ])
            )
        else:
            cnt = VSplit(
                self._append_margin([
                    VSplit(
                        self._append_margin([
                            DynamicContainer(lambda: self._body),
                        ]),
                        padding=0
                    )])
            )

        filler = VSplit([
            VSplit(
                self._append_margin([
                    self._fill(width=1, char=self._border.left if self._show_border else ""),
                    self._fill(char=" "),
                    self._fill(width=1, char=self._border.right if self._show_border else ""),
                ]),
                height=1,
                width=self._width
            )],
            width=self._width
        )

        arr = []
        for _ in range(self._padding[0]):
            arr.append(filler)
        arr.append(cnt)
        for _ in range(self._padding[0]):
            arr.append(filler)

        return HSplit(
            arr,
            height=self._height,
            style=self._style
        )

    def _create_container_arr(self):

        horizontal_margin = VSplit([
            self._fill(height=1, char="")
        ], height=self._margin[0])

        arr = []
        if self._margin[0] > 0:
            arr.append(horizontal_margin)
        if self._show_border:
            arr.append(self._create_top_row())
        arr.append(self._create_main_container())
        if self._show_border:
            arr.append(self._create_bottom_row())
        if self._margin[0] > 0:
            arr.append(horizontal_margin)

        return arr

    def __pt_container__(self) -> Container:
        return self.container


def grom_frame(
        text: AnyFormattedText,
        title: AnyFormattedText | Type[None] = None,
        width: int = None,
        margin: tuple[int] = None,
        padding: tuple[int] = None,
        show_border: bool = True,
        border: BorderChars | str = None,
        align: WindowAlign | str = WindowAlign.CENTER
):
    grom_frame_container(
        FormattedTextControl(text=HTML(text)),
        title, width, margin, padding, show_border, border, align
    )


def grom_frame_container(
        ui_control: UIControl,
        title: AnyFormattedText | Type[None] = None,
        width: int = None,
        margin: tuple[int] = None,
        padding: tuple[int] = None,
        show_border: bool = True,
        border: BorderChars | str = None,
        align: WindowAlign | str = WindowAlign.CENTER
):

    if margin is None or len(margin) < 2:
        margin = (0, 0)

    if padding is None or len(padding) < 2:
        padding = (0, 0)

    def window_width():
        if width is None:
            return None
        if show_border:
            return width - ((padding[1] * 2) + 2) - (margin[1] * 2)
        return width - (padding[1] * 2) - (margin[1] * 2)

    if align and isinstance(align, str):
        if align == "left":
            align = WindowAlign.LEFT
        elif align == "right":
            align = WindowAlign.RIGHT
        elif align == "center":
            align = WindowAlign.CENTER
        else:
            raise NotImplementedError("Unsupported align type")

    print_container(
        _Frame(
            Window(
                ui_control,
                style="class:frame.content",
                align=align,
                wrap_lines=True,
                always_hide_cursor=True,
                width=window_width()
            ),
            title=title,
            show_border=show_border,
            border=border_from_source(border),
            width=width,
            margin=margin,
            padding=padding
        ),
        style=GromThemer().style
    )
