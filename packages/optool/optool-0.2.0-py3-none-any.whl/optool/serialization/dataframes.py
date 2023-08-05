from __future__ import annotations

from typing import Any, Dict

import pandas as pd
import pytz

from optool.serialization import Serializer


class DataFrameSerializer(Serializer[pd.DataFrame]):

    def serialize(self, obj: pd.DataFrame) -> Dict[str, Any]:
        if not isinstance(obj.index, pd.RangeIndex):
            obj = obj.copy()
            index_name = obj.index.name
            obj['non_serializable_index'] = obj.index
            obj = obj.reset_index(drop=True)  # replaces index with RangeIndex
            obj.index.name = index_name

        return obj.to_dict()

    def deserialize(self, raw: Dict[str, Any]) -> pd.DataFrame:
        obj = pd.DataFrame.from_dict(raw)
        if 'non_serializable_index' in obj:
            index_name = obj.index.name
            obj.set_index('non_serializable_index', drop=True, inplace=True)
            obj.index.name = index_name

        return obj


class SeriesSerializer(Serializer[pd.Series]):
    _DICT_KEY_TIMEZONE = 'timezone'

    _DATE_FMT = "%Y-%m-%d %H:%M:%S.%f"
    _DATE_FMT_TZ = _DATE_FMT + " %Z %z"

    def serialize(self, obj: pd.Series) -> Dict[str, Any]:
        if obj.ndim != 1:
            raise ValueError(f"The number of dimensions of a pandas series must be 1, but is {obj.ndim}.")

        if isinstance(obj.index, pd.RangeIndex):
            return obj.to_dict()

        if isinstance(obj.index, pd.DatetimeIndex):
            obj = obj.copy()
            (tz_name, tz_fmt) = (obj.index.tz.zone, self._DATE_FMT_TZ) if obj.index.tz else (None, self._DATE_FMT)
            obj.index = obj.index.strftime(tz_fmt)  # replace the index
            dct = obj.to_dict()
            dct[self._DICT_KEY_TIMEZONE] = tz_name
            return dct
        raise TypeError(f"Cannot serialize a pandas series with index of type {obj.index.__class__.__name__}.")

    def deserialize(self, raw: Dict[str, Any]) -> pd.Series:
        if self._DICT_KEY_TIMEZONE not in raw:
            return pd.Series(raw)

        tz_name = raw.pop(self._DICT_KEY_TIMEZONE)
        obj = pd.Series(raw)
        obj.index = pd.DatetimeIndex(obj.index)  # replace the index
        if tz_name:
            obj.index = obj.index.tz_convert(pytz.timezone(tz_name))  # restore the localized time zone
            if list(raw.keys()) != list(obj.index.strftime(self._DATE_FMT_TZ)):
                raise ValueError("The date-time index does  not have the same time zone anymore.")
        return obj
