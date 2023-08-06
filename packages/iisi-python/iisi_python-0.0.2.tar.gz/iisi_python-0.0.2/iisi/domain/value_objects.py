"""_summary_

Raises:
    ValidationException: _description_

Returns:
    _type_: _description_
"""
from uuid import UUID, uuid4

from iisi.domain.exception import ValidationException


class Id(str):
    """
    Domain id value object.
    """

    def __new__(cls, value):
        """
        Initializes a new instance of Id value object.
        :param value: id as uuid format.
        :return: id value object.
        :raise ValidationException: If value is not a string.
        :raise ValidationException: If value is not valid UUID.
        """
        if isinstance(value, UUID):
            return super().__new__(cls, str(value))
        if not isinstance(value, str):
            raise ValidationException(
                f"{cls.__name__} must be a string, " f"but not '{value}' ({type(value).__name__})"
            )
        try:
            return super().__new__(cls, str(UUID(value)))
        except ValueError as value_error:
            raise ValidationException(
                f"{cls.__name__} must be in valid UUID format."
            ) from value_error

    @classmethod
    def new_id(cls) -> "Id":
        """Factory method for creating a new id."""
        return Id(uuid4())


class MaxLengthString(str):
    """
    Immutable value object representing non-empty and limited length string
    """

    max_length = 0  # override in subclasses

    def __new__(cls, value: str):
        if not isinstance(value, str):
            raise ValidationException(
                f"{cls.__name__} must be a string, " f"but not '{value}' ({type(value).__name__})"
            )
        if len(value) == 0:
            raise ValidationException(f"{cls.__name__} must be not empty")
        if len(value) > cls.max_length:
            raise ValidationException(f"{cls.__name__} is too long ({len(value)}>{cls.max_length})")

        # Value is valid, we can construct it
        return super().__new__(cls, value)  # type: ignore
