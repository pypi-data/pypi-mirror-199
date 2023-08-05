from enum import Enum
from typing import Any, Optional, Sequence


class AggregatorType(Enum):
    """Lists the possible aggregation operations to perform on the data to
    return a measure."""
    SUM = "sum"
    COUNT = "count"
    AVERAGE = "avg"
    MAX = "max"
    MIN = "min"
    MODE = "mode"
    BASICGROUPEDMEDIAN = "basic_grouped_median"
    WEIGHTEDSUM = "weighted_sum"
    WEIGHTEDAVERAGE = "weighted_avg"
    REPLICATEWEIGHTMOE = "replicate_weight_moe"
    CALCULATEDMOE = "moe"
    WEIGHTEDAVERAGEMOE = "weighted_average_moe"

    @classmethod
    def from_str(cls, value: str):
        value = value.lower()
        try:
            return next((item for item in cls if item.value == value))
        except StopIteration:
            raise ValueError(f"Invalid AggregatorType value: {value}")


class DimensionType(Enum):
    """Lists the kinds of data a dimension is storing."""
    STANDARD = "standard"
    TIME = "time"
    GEO = "geo"

    @classmethod
    def from_str(cls, value: Optional[str]):
        if value is None:
            return cls.STANDARD
        value = value.lower()
        return next((item for item in cls if item.value == value), cls.STANDARD)


class MemberType(Enum):
    """Lists the types of the data the user can expect to find in the associated
    column."""
    # TODO: add UInt values
    BOOLEAN = "bool"
    DATE = "date"
    TIME = "time"
    DATETIME = "dttm"
    TIMESTAMP = "stmp"
    FLOAT32 = "f32"
    FLOAT64 = "f64"
    INT8 = "i8"
    INT16 = "i16"
    INT32 = "i32"
    INT64 = "i64"
    STRING = "str"

    def get_caster(self):
        if self in (MemberType.INT8, MemberType.INT16, MemberType.INT32, MemberType.INT64):
            return int
        if self in (MemberType.FLOAT32, MemberType.FLOAT64):
            return float
        if self == MemberType.BOOLEAN:
            return bool
        return str

    @classmethod
    def from_str(cls, value: Optional[str]):
        if value is None:
            return cls.INT64
        value = value.lower()
        return next((item for item in cls if item.value == value), cls.INT64)

    @classmethod
    def from_values(cls, values: Sequence[Any]):
        value = values[0]

        if isinstance(value, bool):
            return MemberType.BOOLEAN

        if isinstance(value, int):
            return cls.from_int_values(values)

        if isinstance(value, float):
            return MemberType.FLOAT64

        if isinstance(value, str):
            if value.isnumeric():
                if int(value) == float(value):
                    return cls.from_int_values([int(i) for i in values])
                return MemberType.FLOAT64

        return MemberType.STRING

    @classmethod
    def from_int_values(cls, values: Sequence[int]):
        mini = min(values)
        maxi = max(values)

        if mini < -2147483648 or maxi > 2147483647:
            return MemberType.INT64
        elif mini < -32768 or maxi > 32767:
            return MemberType.INT32
        elif mini < -128 or maxi > 127:
            return MemberType.INT16
        else:
            return MemberType.INT8
