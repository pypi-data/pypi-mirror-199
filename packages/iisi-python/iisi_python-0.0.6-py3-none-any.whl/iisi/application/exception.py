"""
Module for domain exceptions.
"""


class DomainException(Exception):
    """
    Base object for domain exception.
    """


class ValidationException(DomainException):
    """
    Raised when invalid value is given.
    """


class NotFoundException(DomainException):
    """
    Raised when entity is not found.
    """


class NotAuthorizedException(DomainException):
    """
    Raised when user is not authorized.
    """


class DataException(DomainException):
    """
    Raised when error occurred in repository.
    """
