"""
List of exceptions that may be happen in our new modest framework.
"""

class NotFoundModelException(Exception):
    pass


class ParsingExcpetion(Exception):
    pass


class YamlAttributeNotFoundException(Exception):
    pass


class YamlEntryNotFoundInListException(Exception):
    pass

class NotFoundValidatorException(Exception):
    pass

class InvalidValue(Exception):
    """
    Base form validation exception

    Based on https://github.com/Pylons/colander/blob/master/colander/__init__.py

    """
