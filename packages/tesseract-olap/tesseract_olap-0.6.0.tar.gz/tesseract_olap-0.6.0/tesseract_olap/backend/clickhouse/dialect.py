from enum import Enum
from typing import Union

from pypika.terms import AggregateFunction, Field, Function, Parameter
from pypika.utils import format_alias_sql

from tesseract_olap.schema.enums import MemberType


class ClickhouseDataType(Enum):
    """Lists the types of the data the user can expect to find in the associated
    column."""
    BOOLEAN = "Bool"
    DATE = "Date32"
    DATETIME = "DateTime64"
    TIMESTAMP = "UInt32"
    FLOAT32 = "Float32"
    FLOAT64 = "Float64"
    INT8 = "Int8"
    INT16 = "Int16"
    INT32 = "Int32"
    INT64 = "Int64"
    STRING = "String"

    @classmethod
    def from_membertype(cls, mt: MemberType):
        """Transforms a MemberType enum value into a ClickhouseDataType."""
        return next((item for item in cls if item.name == mt.name), cls.STRING)


class ArrayElement(Function):
    def __init__(self, array, n: int, *args, **kwargs) -> None:
        super().__init__("arrayElement", *args, **kwargs)
        self._array = array
        self._n = n

    def get_sql(
        self, with_alias=False, with_namespace=False, quote_char=None, dialect=None, **kwargs
    ) -> str:
        sql = "{name}({array},{n})".format(
            name=self.name,
            array=self._array.get_sql(),
            n=self._n,
        )
        return format_alias_sql(sql, self.alias, **kwargs)


class TopK(AggregateFunction):
    def __init__(
        self,
        amount: int,
        field: Union[str, Field],
        alias: Union[str, None] = None,
    ):
        super().__init__("topK(%d)" % amount, field, alias=alias)


class StringParameter(Parameter):
    """Bracket style with parameter name, e.g. ...WHERE name = {p0}"""

    def get_sql(self, **kwargs) -> str:
        return "{{{0}:String}}".format(self.placeholder)
