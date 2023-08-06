"""
Grom CLI
"""
import argparse

from grom import grom_frame
from grom.components.frame import Border
from grom.theme import set_theme_from_str

from grom.console.validate import ValidateIntPair, PositiveInt


def _frame(args):
    def str_to_pair(s: str):
        if s is None:
            return None
        arr = list(map(int, s.split()))
        if not len(arr) == 2:
            raise AttributeError("Must be a string of two numbers separated with space")
        return tuple(arr)

    if args.theme:
        set_theme_from_str(args.theme)

    grom_frame(
        text=args.text,
        title=args.title,
        show_border=True if args.show_border is None else args.show_border,
        width=args.width,
        border=args.border,
        align=args.align,
        margin=str_to_pair(args.margin),
        padding=str_to_pair(args.padding)
    )


def _frame_parser(subparsers):
    p = subparsers.add_parser('frame', help='Apply bordering, borders, spacing to text')
    p.add_argument('--text', type=str, help='Text content to show within the frame')
    p.add_argument('--title', type=str, help='Title to show in border if border is show', default=None)
    p.add_argument('--border', type=str, help='Select border style', default='rounded',
                   choices=list(map(lambda f: f.name.lower(), list(Border))))
    p.add_argument('--show_border', help='Show border', action=argparse.BooleanOptionalAction)
    p.add_argument('--width', type=int, help='The frame width. Default is full width', default=None, action=PositiveInt)
    p.add_argument('--align', type=str, help='Text alignment', default='center',
                   choices=['left', 'right', 'center'])
    p.add_argument('--theme', type=str, help='Select theme', default='default',
                   choices=['default', 'desert', 'forest', '8bit'])
    p.add_argument('--padding', type=str, help="Text padding", default=None, action=ValidateIntPair)
    p.add_argument('--margin', type=str, help="Text margin", default=None, action=ValidateIntPair)
    p.set_defaults(func=_frame)


def _progress_bar_parser(subparsers):
    p = subparsers.add_parser(
        'progress', help='Show a simple progress bar (Advanced features from witin Python)')
    p.add_argument('--baz', choices='XYZ', help='baz help')


def _spinner_parser(subparsers):
    p = subparsers.add_parser('spinner', help='Show simple spinner (Advanced features from within Python)')
    p.add_argument('--baz', choices='XYZ', help='baz help')


def run():
    parser = argparse.ArgumentParser(
        prog='Grom',
        description="A tool for amazing shell and Python scripts.",
    )
    parser.add_argument('--version', action='store_true', help='Print the version number')
    subparsers = parser.add_subparsers(help='sub-command help')

    _frame_parser(subparsers)
    _progress_bar_parser(subparsers)
    _spinner_parser(subparsers)

    args = parser.parse_args()
    method = getattr(args, 'func', None)

    args.func(args) if callable(method) else parser.print_help()
