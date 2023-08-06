"""
Helper functions for the Grom argparse client.
"""
import argparse
import re


class ValidateIntPair(argparse.Action):
    """
    Validator checking if a given string contains a pair of numbers separated with a space.
    """

    def __call__(self, parser, namespace, values, _=None):
        pattern = re.compile(r'^\d*.\d*$')

        if not pattern.match(values):
            parser.error("Must be a pair of two numbers separated by a space. eg: '4 2'")
        setattr(namespace, self.dest, values)


class PositiveInt(argparse.Action):
    """
    Validator checking if a given int is a positive number over 0.
    """

    def __call__(self, parser, namespace, values, _=None):
        if values < 1:
            parser.error("Must be a positive number over 0")
        setattr(namespace, self.dest, values)
