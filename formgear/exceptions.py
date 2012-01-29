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

