"""
Grom theming
"""
from dataclasses import dataclass
from enum import Enum

from prompt_toolkit.styles import Style
from prompt_toolkit.output.color_depth import ColorDepth

from grom.tools import Singleton


@dataclass(frozen=True)
class GromSpinnerStyle:
    """_summary_"""

    frames: list[str]
    done_frame: str
    stopped_frame: str
    fps: int


class GromSpinnerStyles(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """

    LINE = GromSpinnerStyle(["|", "/", "-", "\\"], "✓", "ⅹ", 2)
    DOT = GromSpinnerStyle(["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"], "✓", "!", 3)
    MINIDOT = GromSpinnerStyle(
        ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"], "✓", "⚠", 3
    )
    JUMP = GromSpinnerStyle(["⢄", "⢂", "⢁", "⡁", "⡈", "⡐", "⡠"], "✓", "⚠", 3)
    PULSE = GromSpinnerStyle(["█", "▓", "▒", "░"], "✓", "⚠", 2)
    POINTS = GromSpinnerStyle(["∙∙∙", "●∙∙", "∙●∙", "∙∙●"], "✓", "⚠", 2)
    GLOBE = GromSpinnerStyle(["🌍", "🌎", "🌏"], "✓", "⚠", 2)
    MOON = GromSpinnerStyle(["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"], "✓", "⚠", 3)
    MONKEY = GromSpinnerStyle(["🙈", "🙉", "🙊"], "✓", "⚠", 2)
    METER = GromSpinnerStyle(
        ["▱▱▱", "▰▱▱", "▰▰▱", "▰▰▰", "▰▰▱", "▰▱▱", "▱▱▱"], "✓", "⚠", 2
    )
    HAMBURGER = GromSpinnerStyle(["☱", "☲", "☴", "☲"], "✓", "⚠", 3)


@dataclass
class GromThemeColors:
    """
    Color theme class with defaults
    """

    main_foreground: str = "#ffffff"
    main_background: str = None
    secondary_foreground: str = "#7571F9"
    secondary_background: str = None
    highlight_foreground: str = "#ff87d7"
    highlight_background: str = None
    gradient_start: str = None
    gradient_end: str = None
    shaded_foreground: str = "#606060"
    shaded_background: str = None

    def __post_init__(self):
        self.gradient_start = self.secondary_foreground
        self.gradient_end = self.highlight_foreground


@dataclass
class GromTheme:
    """
    Grom theme lets you customize default colors in use by Grom formatters and components.
    """
    colors: GromThemeColors
    color_depth: ColorDepth = ColorDepth.DEPTH_24_BIT
    spinner_style: GromSpinnerStyle = GromSpinnerStyles.DOT.value
    margin_horizontal = 1
    margin_vertical = 1


def default_theme() -> GromTheme:
    return GromTheme(
        GromThemeColors(),
        color_depth=ColorDepth.DEPTH_24_BIT
    )


def eight_bit_theme() -> GromTheme:
    return GromTheme(
        GromThemeColors(
            main_foreground="white",
            highlight_foreground="yellow"
        ),
        color_depth=ColorDepth.DEPTH_8_BIT
    )


def desert_theme() -> GromTheme:
    return GromTheme(
        GromThemeColors(
            main_foreground="#FFFFFF",
            secondary_foreground="#A07855",
            highlight_foreground="#D4B996"
        )
    )


def forest_theme() -> GromTheme:
    return GromTheme(GromThemeColors(main_foreground="white", secondary_foreground="#2C5F2D", highlight_foreground="#97BC62"))


class GromThemer(metaclass=Singleton):
    """
    Grom theme holder class
    """

    def __init__(self) -> None:
        self._theme = GromTheme(GromThemeColors())
        self._style = self._create_style()

    @property
    def theme(self) -> GromTheme:
        """
        Get the current set theme
        """
        return self._theme

    @theme.setter
    def theme(self, value: GromTheme) -> None:
        """
        Set a new theme
        """
        assert isinstance(value, GromTheme)
        self._theme = value
        self._style = self._create_style()

    @property
    def style(self) -> Style:
        """
        Get the current set style
        """
        return self._style

    def _color_str(self, background_color: str, foreground_color: str):
        color_str = ""
        if foreground_color:
            color_str = f" fg:{foreground_color}"
        if background_color:
            color_str = f" {color_str} bg:{background_color}"
        return color_str

    def _create_style(self):
        colors = self._theme.colors
        return Style.from_dict(
            {
                "progressbar title": f"{colors.main_foreground} bold",
                "progressbar": self._color_str(colors.highlight_background, colors.highlight_foreground),
                "progressbar-bg": self._color_str(colors.shaded_background, colors.shaded_foreground),
                "time-left": f"{colors.highlight_foreground}",
                "spinning-wheel": f"{colors.highlight_foreground}",
                "bottom-toolbar": self._color_str(colors.shaded_background, colors.shaded_foreground),
                "bottom-toolbar.text": self._color_str(colors.shaded_background, colors.shaded_foreground),
                "frame.border": self._color_str(colors.highlight_background, colors.highlight_foreground),
                "frame.content": self._color_str(colors.main_background, colors.main_foreground),
                "frame.title": self._color_str(colors.highlight_background, colors.highlight_foreground),
            }
        )


def spinner_style_from_arg(arg: GromSpinnerStyles | GromSpinnerStyle | None):
    if isinstance(arg, Enum):
        if isinstance(arg.value, GromSpinnerStyle):
            return arg.value
        return GromThemer().theme.spinner_style
    if isinstance(arg, GromSpinnerStyle):
        return arg
    return GromThemer().theme.spinner_style


def set_theme_from_str(t: str):
    if t and isinstance(t, str):
        if t == "default":
            t = default_theme()
        elif t == "forest":
            t = forest_theme()
        elif t == "8bit":
            t = eight_bit_theme()
        elif t == "desert":
            t = desert_theme()
        else:
            raise NotImplementedError("Unsupported theme name")
        GromThemer().theme = t
