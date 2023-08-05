from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, Any, Dict, Generic, Optional, TypeVar

from pint import Unit
from pydantic import ValidationError
from pydantic.errors import PydanticTypeError, PydanticValueError
from pydantic.fields import ModelField
from pydantic.utils import update_not_none

from optool.fields.util import WrongTypeError, check_validation_is_passed_on_to_sub_types, get_type_validator
from optool.uom import UNITS, PhysicalDimension, Quantity


class DimensionalityError(PydanticValueError):

    def __init__(self, *, expected: str, value: Quantity) -> None:
        super().__init__(expected=expected, actual=value.dimensionality)

    msg_template = 'expected the dimensionality {expected}, but got a value with dimensionality {actual}'


class UnsupportedMagnitudeConversion(PydanticTypeError):

    def __init__(self, *, value: Any) -> None:
        super().__init__(type=type(value))

    msg_template = 'the value of {type} cannot be converted automatically'


class UnitParseError(PydanticValueError):

    def __init__(self, *, unit: str) -> None:
        super().__init__(unit=unit)

    msg_template = 'cannot parse the unit {unit}'


class ConstrainedUnit(Unit):
    """
    Pydantic-compatible field type for :py:class:`pint.Unit` objects, which allows to specify the desired
    dimensionality.

    See Also:
        `Pydantic documentation: Custom Data Types <https://docs.pydantic.dev/usage/types/#custom-data-types>`_ and
        class :py:class:`pydantic.types.ConstrainedInt` or similar of :py:mod:`pydantic`
    """
    strict: bool = False
    dimensionality: Optional[str] = None

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        update_not_none(
            field_schema,
            dimensionality=cls.dimensionality,
        )

    @classmethod
    def __get_validators__(cls):
        yield get_type_validator(Unit) if cls.strict else cls.validate_unit
        yield cls.validate_dimensionality

    @classmethod
    def validate_unit(cls, value: Any, field: ModelField) -> Unit:
        if isinstance(value, Unit):
            return value

        if isinstance(value, str):
            try:
                return UNITS.parse_units(value)
            except Exception as e:
                raise UnitParseError(unit=value) from e

        raise WrongTypeError(expected=(Unit, str), value=value)

    @classmethod
    def validate_dimensionality(cls, value: Unit) -> Unit:
        if cls.dimensionality is None or value.dimensionality == UNITS.get_dimensionality(cls.dimensionality):
            return value
        raise DimensionalityError(expected=cls.dimensionality, value=value)


T = TypeVar("T")  # Allow storing anything as magnitude in Quantity
D = TypeVar("D", bound=PhysicalDimension)


class ConstrainedQuantity(Quantity, Generic[D, T]):  # TODO try to switch arguments
    """
    Pydantic-compatible field type for :py:class:`pint.Quantity` objects, which allows to specify the desired
    dimensionality.

    See Also:
        Class :py:class:`pydantic.types.ConstrainedInt` or similar of :py:mod:`pydantic`.
    """

    strict: bool = False

    # gt: Optional[] = None
    # ge: OptionalInt = None
    # lt: OptionalInt = None
    # le: OptionalInt = None

    @classmethod
    def __get_validators__(cls):
        yield get_type_validator(Quantity, lambda x: type(x.m)) if cls.strict else cls.validate_quantity
        yield cls.validate_dimensionality
        yield cls.validate_magnitude

    @classmethod
    def validate_quantity(cls, val: Any, field: ModelField) -> Quantity:
        try:
            return Quantity(val)
        except Exception as e:
            raise WrongTypeError(expected=(Quantity, str, Number), value=val) from e

    @classmethod
    def validate_dimensionality(cls, val: Quantity, field: ModelField) -> Quantity:
        if not field.sub_fields or field.sub_fields[0].type_ == Any:
            return val

        dimension = field.sub_fields[0].type_
        if not issubclass(dimension, PhysicalDimension):
            raise TypeError(f"Unsupported {dimension}, should be a {PhysicalDimension.__name__!r} or 'typing.Any'.")
        elif not val.check(dimension.dimensionality):
            raise DimensionalityError(expected=dimension.dimensionality, value=val)
        return val

    @classmethod
    def validate_magnitude(cls, val: Quantity, field: ModelField) -> Quantity:
        if not field.sub_fields:
            return val

        magnitude_field = field.sub_fields[1]
        check_validation_is_passed_on_to_sub_types(field.name, magnitude_field)
        valid_value, error = magnitude_field.validate(val.m, {}, loc='magnitude')
        if error:
            raise ValidationError([error], cls)

        return Quantity(valid_value, val.u)


if TYPE_CHECKING:
    UnitLike = Unit

    QuantityLike = Quantity

else:

    class UnitLike(ConstrainedUnit):
        strict = False

    class QuantityLike(ConstrainedQuantity[D, T]):
        pass
