from typing import TYPE_CHECKING

from pydantic import ConstrainedFloat, ConstrainedStr

if TYPE_CHECKING:
    NonEmptyStr = str
    PositiveFiniteFloat = float

else:

    class NonEmptyStr(ConstrainedStr):
        strict = True
        strip_whitespace = True
        min_length = 1

    class PositiveFiniteFloat(ConstrainedFloat):
        strict = False
        gt = 0
        allow_inf_nan = False
