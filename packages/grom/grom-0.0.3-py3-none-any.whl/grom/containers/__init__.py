"""
Module for shared conditional containers
"""

from prompt_toolkit.filters import Condition, is_done, renderer_height_is_known
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.layout import ConditionalContainer, FormattedTextControl, Window

from grom.theme import GromThemer


def margin_container():
    return ConditionalContainer(
        Window(
            FormattedTextControl(lambda: ""),
            height=GromThemer().theme.margin_horizontal,
            style="",
        ),
        filter=Condition(lambda: True)
    )


def title_container(title: str):
    return ConditionalContainer(
        Window(
            FormattedTextControl(lambda: f"{' ' * GromThemer().theme.margin_vertical}{title}"),
            height=2,
            style="class:progressbar,title",
        ),
        filter=Condition(lambda: title is not None)
    )


def bottom_toolbar_container(bottom_toolbar: AnyFormattedText):
    return ConditionalContainer(
        Window(
            FormattedTextControl(
                lambda: bottom_toolbar, style="class:bottom-toolbar.text"
            ),
            style="class:bottom-toolbar",
            height=1,
        ),
        filter=~is_done &  # pylint: disable=E1130
        renderer_height_is_known &
        Condition(lambda: bottom_toolbar is not None),
    )
