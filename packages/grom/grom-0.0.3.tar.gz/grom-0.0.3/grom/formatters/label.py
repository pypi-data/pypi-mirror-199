"""
Text Formatter

Requires the properties label and counters on the child object (V).

"""
import time
from typing import TYPE_CHECKING

from prompt_toolkit.formatted_text import (
    AnyFormattedText,
    StyleAndTextTuples,
    to_formatted_text,
)

from prompt_toolkit.formatted_text.utils import fragment_list_width
from prompt_toolkit.layout.dimension import AnyDimension, D
from prompt_toolkit.layout.utils import explode_text_fragments

from .format import Formatter

if TYPE_CHECKING:
    from .format import T, V


class Label(Formatter["T", "V"]):
    """
    Display the name of the current task.

    :param width: If a `width` is given, use this width. Scroll the text if it
        doesn't fit in this width.
    :param suffix: String suffix to be added after the task name, e.g. ': '.
        If no task name was given, no suffix will be added.
    """

    def __init__(self, width: AnyDimension = None, suffix: str = "") -> None:
        self.width = width
        self.suffix = suffix

    def _add_suffix(self, label: AnyFormattedText) -> StyleAndTextTuples:
        label = to_formatted_text(label, style="class:label")
        return label + [("", self.suffix)]

    def format(
        self,
        component: "T",
        child: "V[object]",
        width: int,
    ) -> AnyFormattedText:

        label = self._add_suffix(child.label)
        cwidth = fragment_list_width(label)

        if cwidth > width:
            # It doesn't fit -> scroll task name.
            label = explode_text_fragments(label)
            max_scroll = cwidth - width
            current_scroll = int(time.time() * 3 % max_scroll)
            label = label[current_scroll:]

        return label

    def get_width(self, component: "T") -> AnyDimension:
        if self.width:
            return self.width

        all_labels = [self._add_suffix(c.label) for c in component.counters]
        if all_labels:
            max_widths = max(fragment_list_width(lbl) for lbl in all_labels)
            return D(preferred=max_widths, max=max_widths)
        return D()
