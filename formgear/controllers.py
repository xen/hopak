# -*- coding: utf-8 -*-
#

""" Basic validators
"""
import re
from formgear.exceptions import NotFoundValidatorException, InvalidValue
from registry import Registry

import sys

PY3 = sys.version_info[0] == 3

if PY3: # pragma: no cover
    string_types = str,
    text_type = str
else:
    string_types = basestring,
    text_type = unicode

class ValidatorRegistry(Registry):
    NotFound = NotFoundValidatorException

class MetaValidator(type):
    """
    Class for all validators
    """
    def __new__(cls, name, bases, attrs):
        registername = attrs.pop('name', name.lower())
        newbornclass = super(MetaValidator, cls).__new__(cls, name, bases, attrs)
        ValidatorRegistry.register(newbornclass, registername)
        return newbornclass

class BaseValidator(object):
    """ All vaidators should be child of this class to add themself to registry
    """
    __metaclass__ = MetaValidator


class Required(BaseValidator):
    """ Validator which tests is value empty."""
    def __init__(self):
        pass

    def __call__(self, node):
        if not node:
            raise InvalidValue(node, "is required")

class Max(BaseValidator):
    def __init__(self, max):
        self.max = max

    def __call__(self, node):
        if node > self.max:
            raise InvalidValue(node, "more then max=%s" % str(self.max))

class Min(BaseValidator):
    def __init__(self, min):
        self.min = min

    def __call__(self, node):
        if node < self.min:
            raise InvalidValue(node, "less then min=%s" % str(self.min))

class Regex(BaseValidator):
    def __init__(self, regex, msg=None):
        if isinstance(regex, string_types):
            self.match_object = re.compile(regex)
        else:
            self.match_object = regex
        if msg is None:
            self.msg = "String does not match expected pattern"
        else:
            self.msg = msg

    def __call__(self, node, value):
        if self.match_object.match(value) is None:
            raise InvalidValue(node, self.msg)

class Email(Regex):
    """ Email address validator.
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = _("Invalid email address")
        super(Email, self).__init__(regex='(?i)^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$', msg=msg)

class Length(BaseValidator):
    """ Validator which succeeds if the value passed to it has a
    length between a minimum and maximum.  The value is most often a
    string."""
    min_err = 'Shorter than minimum length %s'
    max_err = 'Longer than maximum length %s'

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def __call__(self, node, value):
        if self.min is not None:
            if len(value) < self.min:
                raise InvalidValue(node, self.min_err % str(self.min))

        if self.max is not None:
            if len(value) > self.max:
                raise InvalidValue(node, self.max_err % str(self.max))
