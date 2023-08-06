from typing import Tuple, List
from dataclasses import dataclass


def hue_to_rgb(hue: float) -> Tuple[int, int, int]:
    """
    Take hue between 0 and 1, return (r, g, b).
    """
    i = int(hue * 6.0)
    f = (hue * 6.0) - i

    q = int(255 * (1.0 - f))
    t = int(255 * (1.0 - (1.0 - f)))

    i %= 6

    return [
        (255, t, 0),
        (q, 255, 0),
        (0, 255, t),
        (0, q, 255),
        (t, 0, 255),
        (255, 0, q),
    ][i]


@dataclass
class RGB:
    """RGB color dataholder"""
    r: int
    g: int
    b: int

    def to_hex(self) -> str:
        """Convert RGB color into hex string"""
        return ('#{:X}{:X}{:X}').format(self.r, self.g, self.b)  # pylint: disable=C0209


def hex_to_rgb(hex_color) -> RGB:
    """
    Convert a hex color (#FFFFFF) to an RGB color class.
    """
    t = tuple(int(hex_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    return RGB(t[0], t[1], t[2])


def lerp(a: RGB, b: RGB, t: float) -> RGB:
    """
    https://dev.to/ndesmic/linear-color-gradients-from-scratch-1a0e
    """
    return RGB(
        r=round(a.r + (b.r - a.r) * t),
        g=round(a.g + (b.g - a.g) * t),
        b=round(a.b + (b.b - a.b) * t)
    )


def gradient(start_color: str, end_color: str, steps: int) -> List[RGB]:
    stc = hex_to_rgb(start_color)
    ste = hex_to_rgb(end_color)
    if not steps or steps < 1:
        return []
    return [lerp(stc, ste, i / (steps - 1)) for i in range(steps)]
