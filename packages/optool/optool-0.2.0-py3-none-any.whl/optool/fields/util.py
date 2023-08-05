from __future__ import annotations

import re
from typing import Any, Callable, Iterable, Optional, Type, TypeVar, Union

from pydantic.errors import PydanticTypeError, PydanticValueError
from pydantic.fields import ModelField
from pydantic.validators import find_validators

from optool import BaseModel

TypeDefinition = Union[type, tuple[type, ...]]
ValidationFunc = Callable[[Any], Any]

T = TypeVar("T")


class WrongTypeError(PydanticTypeError):

    def __init__(self, *, expected: TypeDefinition, value: Any) -> None:
        super().__init__(expected=expected, actual=type(value))
        self.msg_template = 'expected {expected}, but got {actual}'


class WrongSubTypeError(PydanticTypeError):

    def __init__(self, *, expected_type: TypeDefinition, expected_subtype: TypeDefinition,
                 actual_subtype: TypeDefinition, value: Any) -> None:
        super().__init__(expected_type=expected_type,
                         expected_subtype=expected_subtype,
                         actual_subtype=actual_subtype,
                         actual_type=type(value))
        self.msg_template = 'expected sub-type {expected_subtype} of {expected_type}, ' \
                            'but got {actual_subtype} of {actual_type}'


class ArbitrarySubTypeError(PydanticTypeError):

    def __init__(self, *, name: str, field: ModelField) -> None:
        sub_type = None if field.sub_fields is None else field.sub_fields[0].type_
        super().__init__(name=name, type=field.type_, sub_type=sub_type)
        self.msg_template = 'the sub-field of {name!r} has the type {type} (with sub-type {sub_type}), but {type} ' \
                            'does not offer any specific validators that would be able to handle sub-types'


class ValidationFunctionError(PydanticValueError):

    def __init__(self, *, value: Any, msg_template: Optional[str] = None) -> None:
        super().__init__(value=value)
        if msg_template:
            self.msg_template = msg_template


class _ConfigWithArbitraryTypesNotAllowed(BaseModel.Config):
    arbitrary_types_allowed = False


def has_specific_type_validator(type_: Type[Any]) -> bool:
    """
    Determines if the type specified has one or more validators that are more specific than just the
    ``arbitrary_type_validator`` that is used when ``arbitrary_types_allowed`` of Config is set to True.

    Args:
        type_: The type to analyze

    Returns:
        True if the type specified has a validator that is different from the arbitrary_type_validator, False otherwise.
    """

    try:
        next(find_validators(type_, _ConfigWithArbitraryTypesNotAllowed))
        return True
    except Exception as e:
        if re.match("no validator found for <.*?>, see `arbitrary_types_allowed` in Config", str(e)):
            return False
        raise e


def check_validation_is_passed_on_to_sub_types(name: str, field: ModelField) -> None:
    if field.sub_fields is None:
        return
    if not has_specific_type_validator(field.type_):
        raise ArbitrarySubTypeError(name=name, field=field)
    for sub_field in field.sub_fields:
        check_validation_is_passed_on_to_sub_types(field.name, sub_field)


def check_sub_fields_level(field: ModelField) -> None:
    if field.sub_fields is None:
        return
    if field.sub_fields[0].sub_fields:
        raise ValueError(f"Generic types more than one level deep are currently not supported. "
                         f"Got {field.sub_fields[0].type_} and {field.sub_fields[0].sub_fields[0].type_}.")


def get_type_validator(expected: Type[T],
                       subtype_provider: Optional[Callable[[T], type]] = None) -> Callable[[Any, ModelField], T]:
    """
    Creates a validation function that checks if the input argument is of the expected type.

    Args:
        expected: The type the resulting validator will enforce.
        subtype_provider: Callable to get the subtype of the provided value.

    Returns:
        A new function that can be used to validate if an input value is an instance of the type specified.
    """

    def validate_type(value: Any, field: ModelField) -> T:
        if not isinstance(value, expected):
            raise WrongTypeError(expected=expected, value=value)

        if field.sub_fields is not None and subtype_provider is not None:
            expected_subtype = field.sub_fields[0].type_
            actual_subtype = subtype_provider(value)
            if expected_subtype != actual_subtype:
                raise WrongSubTypeError(expected_type=expected,
                                        expected_subtype=expected_subtype,
                                        actual_subtype=actual_subtype,
                                        value=value)
            check_sub_fields_level(field)

        return value

    return validate_type


def check_only_one_specified(first: Any, second: Any, message: str) -> None:
    first_present = first if isinstance(first, bool) else first is not None
    second_present = second if isinstance(second, bool) else second is not None
    if first_present and second_present:
        raise ValueError(message)


def validate(value: T,
             validators: Union[bool, ValidationFunc, Iterable[ValidationFunc]],
             msg_template: Optional[str] = None) -> T:
    """
    Validates a given value based on the validator function(s) specified.

    Args:
        value: The value to validate.
        validators: The validator function(s).
        msg_template: The message to show in case the validation fails, may contain ``{value}`` to refer to the value.

    Returns:
        The given value in case the validation is successful.
    """
    if isinstance(validators, bool):
        if validators:
            return value
        raise ValidationFunctionError(value=value, msg_template=msg_template)

    for validator in validators if isinstance(validators, Iterable) else [validators]:
        try:
            satisfied = validator(value)
        except Exception as e:
            raise ValidationFunctionError(value=value, msg_template=msg_template) from e

        if not satisfied:
            raise ValidationFunctionError(value=value, msg_template=msg_template)

    return value


def validate_each(value: Iterable,
                  validators: Union[bool, ValidationFunc, Iterable[ValidationFunc]],
                  msg_template: Optional[str] = None) -> None:
    for (i, element) in enumerate(value):
        validate(element, validators, f'While validating element {i}: {msg_template}')
