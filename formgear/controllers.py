# -*- coding: utf-8 -*-
#

""" Basic validators
"""


class Invalid(Exception):
    """
    Base form validation exception

    Based on https://github.com/Pylons/colander/blob/master/colander/__init__.py

    """

class Required(object):
    """ Validator which tests is value empty."""
    def __init__(self):
        pass

    def __call__(self, node):
        if not node:
            raise Invalid(node, "is required")
