import csv
from email.message import Message
from typing import Generator, Iterable, List, Sequence, Tuple, Union

DELIMITER_TRANSLATE = {
    "comma": ",",
    "semicolon": ";",
    "tab": "\t",
    "space": " ",
}


def parse_csv(
    content: Iterable[str],
    *,
    dialect: Union[str, csv.Dialect] = "",
    mimetype: str = "",
    **kwargs
) -> List[Tuple[Union[float, str], ...]]:
    """
    General use function to parse a CSV string, from an external source.

    `kwargs` are the parameters to define a :class:`csv.Dialect`.
    """
    dialects = csv.list_dialects()
    if isinstance(dialect, csv.Dialect) or dialect in dialects:
        return [tuple(item) for item in csv.reader(content, dialect)]

    if mimetype:
        msg = Message()
        msg.add_header("Content-Type", mimetype)
        options = dict(msg.get_params(failobj=[], header="Content-Type")[1:])

        dialect = options.get("dialect", "")
        if dialect != "":
            return parse_csv(content, dialect=dialect)

        kwargs.update(options)

    if "delimiter" in kwargs:
        delimiter = kwargs["delimiter"]
        kwargs["delimiter"] = DELIMITER_TRANSLATE.get(delimiter, delimiter)

    content = ColumnTypeInferrer(content, kwargs)
    table = tuple(csv.reader(content, **kwargs))
    return list(content.cast(table))


class ColumnTypeInferrer:
    def __init__(self, iterable: Iterable[str], csv_params: dict):
        self.csv_params = csv_params
        self.headers = ""
        self.iterator = iter(iterable)

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self.iterator)
        if self.headers:
            row_items = next(csv.reader([row], **self.csv_params))
            self.types = [
                itype and item.isnumeric()
                for item, itype in zip(row_items, self.types)
            ]
        else:
            self.headers = list(csv.reader(row))
            self.types = [True for item in self.headers]
        return row

    def cast(
        self, table: Iterable[Sequence[str]],
    ) -> Generator[Tuple[Union[float, str],...], None, None]:
        iterator = iter(table)
        yield tuple(next(iterator))
        yield from (
            tuple(
                numerify(item) if is_num else item
                for item, is_num in zip(row, self.types)
            )
            for row in iterator
        )


def numerify(string: str):
    return int(string) if int(string) == float(string) else float(string)
