from __future__ import annotations

from typing import Any, Dict

from pint import Unit
from pint.util import to_units_container

from optool.serialization import Serializer
from optool.uom import UNITS, Quantity


class QuantitySerializer(Serializer[Quantity]):

    def serialize(self, obj: Quantity) -> Dict[str, Any]:
        return {'mag': obj.m, 'unit': obj.u}

    def deserialize(self, raw: Dict[str, Any]) -> Quantity:
        return Quantity(raw['mag'], raw['unit'])


class UnitSerializer(Serializer[Unit]):

    def serialize(self, obj: Unit) -> Dict[str, Any]:
        return dict(to_units_container(obj))

    def deserialize(self, raw: Dict[str, Any]) -> Unit:
        return UNITS.Unit(UNITS.UnitsContainer(raw))
