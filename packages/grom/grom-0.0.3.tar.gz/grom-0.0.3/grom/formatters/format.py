"""
Formatter classes
"""
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.layout.dimension import AnyDimension, D

T = TypeVar("T")
V = TypeVar("V")


class Formatter(Generic[T, V], metaclass=ABCMeta):
    """
    Base class for any formatter.
    """

    @abstractmethod
    def format(
        self,
        component: "T",
        child: "V[object]",
        width: int,
    ) -> AnyFormattedText:
        pass

    def get_width(self, component: "T") -> AnyDimension:  # pylint: disable=unused-argument
        return D()
