"""XML Schema parsing module

Defines subclasses for the core Entity classes, parsed from an XML document.
"""

import logging
from ast import literal_eval as eval_tuple
from collections import OrderedDict
from pathlib import Path
from typing import (Generator, Iterable, List, Optional, TextIO, Tuple, Type,
                    TypeVar, Union)

import httpx
import immutables as immu
from lxml import etree

from . import models
from .aggregators import Aggregator
from .csv import parse_csv
from .enums import AggregatorType, DimensionType, MemberType
from .exceptions import InvalidXMLAttributeValue, MissingXMLAttribute, MissingXMLNode

logger = logging.getLogger(__name__)

XMLEntity = Union[
    "XMLSharedDimension",
    "XMLHierarchy",
    "XMLLevel",
    "XMLProperty",
    "XMLInlineTable",
    "XMLCube",
    "XMLDimensionUsage",
    "XMLHierarchyUsage",
    "XMLLevelUsage",
    "XMLPropertyUsage",
    "XMLPrivateDimension",
    "XMLMeasure",
]

AnyXMLEntity = TypeVar("AnyXMLEntity", bound=XMLEntity)


class XMLSchema(models.Schema):
    tag = "Schema"

    @classmethod
    def parse(cls, node: etree._Element):
        """Parse a <Schema> XML node."""
        cube_gen = _yield_children_nodes(node, XMLCube)
        shareddim_gen = _yield_children_nodes(node, XMLSharedDimension)
        sharedtbl_gen = _yield_children_nodes(node, XMLInlineTable)

        return cls(
            name=_get_attr(node, "name"),
            cube_map=OrderedDict(cube_gen),
            shared_dimension_map=immu.Map(shareddim_gen),
            shared_table_map=immu.Map(sharedtbl_gen),
            default_locale=node.get("default_locale", "xx"),
            annotations=immu.Map(_yield_annotations(node)),
        )


class XMLCube(models.Cube):
    tag = "Cube"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <Cube> XML node."""
        cube_name = _get_attr(node, "name")

        table = _find_table_ref(node)
        if table is None:
            raise MissingXMLNode(node.tag, cube_name, "Table")

        dimension_map = OrderedDict(
            _yield_children_nodes(node, XMLPrivateDimension, XMLDimensionUsage)
        )
        if len(dimension_map) == 0:
            raise MissingXMLNode(node.tag, cube_name, "Dimension")

        measure_map = OrderedDict(_yield_children_nodes(node, XMLMeasure))
        if len(measure_map) == 0:
            raise MissingXMLNode(node.tag, cube_name, "Measure")

        return cls(
            name=cube_name,
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
            dimension_map=dimension_map,
            measure_map=measure_map,
            table=table,
            annotations=immu.Map(_yield_annotations(node)),
        )


class XMLDimensionUsage(models.DimensionUsage):
    tag = "DimensionUsage"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <DimensionUsage> XML node."""
        return cls(
            name=_get_attr(node, "name"),
            source=_get_attr(node, "source"),
            foreign_key=node.get("foreign_key"),
            annotations=immu.Map(_yield_annotations(node)),
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
            hierarchy_map=OrderedDict(
                _yield_children_nodes(node, XMLHierarchyUsage, attr="source")
            ),
        )


class XMLHierarchyUsage(models.HierarchyUsage):
    tag = "HierarchyUsage"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <HierarchyUsage> XML node."""
        return cls(
            name=_get_attr(node, "name"),
            source=_get_attr(node, "source"),
            annotations=immu.Map(_yield_annotations(node)),
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
            level_map=OrderedDict(
                _yield_children_nodes(node, XMLLevelUsage, attr="source")
            ),
        )


class XMLLevelUsage(models.LevelUsage):
    tag = "LevelUsage"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <LevelUsage> XML node."""
        return cls(
            name=_get_attr(node, "name"),
            source=_get_attr(node, "source"),
            annotations=immu.Map(_yield_annotations(node)),
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
            property_map=OrderedDict(
                _yield_children_nodes(node, XMLPropertyUsage, attr="source")
            ),
        )


class XMLPropertyUsage(models.PropertyUsage):
    tag = "PropertyUsage"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <PropertyUsage> XML node."""
        return cls(
            name=_get_attr(node, "name"),
            source=_get_attr(node, "source"),
            annotations=immu.Map(_yield_annotations(node)),
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
        )


class XMLTable(models.Table):
    tag = "Table"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <Table> XML node."""
        return cls(
            name=_get_attr(node, "name"),
            schema=node.get("schema"),
            primary_key=node.get("primary_key"),
        )


class XMLInlineTable(models.InlineTable):
    tag = "InlineTable"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <InlineTable> XML node."""
        node_name = _get_attr(node, "name")
        node_format = _get_attr(node, "format")

        if node_format == "csv":
            node_format = "text/csv"

        if node_format == "tuples":
            headers, rows = cls.parse_tuples(node)
        elif node_format.startswith("text/csv"):
            content = [] if node.text is None else node.text.strip().splitlines()
            headers, *rows = parse_csv(content, mimetype=node_format)
        else:
            raise InvalidXMLAttributeValue(node.tag, node_name, "format", node_format)

        return cls(
            name=node_name,
            headers=headers,
            types=tuple(MemberType.from_values(column) for column in zip(*rows)),
            rows=rows,
        )

    @staticmethod
    def parse_tuples(node: etree._Element):
        """Parse the child nodes from an InlineTable with `tuples` format."""
        try:
            # try parsing literal tuples with ast.eval()
            children: List[Tuple[str, ...]] = [
                eval_tuple(line)
                for line in (item.text for item in node.iterchildren("Row"))
                if line
            ]
        except SyntaxError:
            # Python `tuples` looks similar to CSV, so let's try with it
            row_iter = (
                line[1:-1] if line.startswith("(") and line.endswith(")") else line
                for line in (item.text for item in node.iterchildren("Row"))
                if line is not None
            )
            children = parse_csv(row_iter, skipinitialspace=True)
        # at least 2 rows must be present: a header list and a data row
        if len(children) < 2:
            raise MissingXMLNode(node.tag, _get_attr(node, "name"), "Row")
        return children[0], children[1:]


class XMLSharedDimension(models.Dimension):
    tag = "SharedDimension"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a Shared <Dimension> XML node."""
        dim_type = node.get("type")

        return cls(
            name=_get_attr(node, "name"),
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
            dim_type=DimensionType.from_str(dim_type),
            foreign_key=node.get("foreign_key"),
            hierarchy_map=OrderedDict(_yield_children_nodes(node, XMLHierarchy)),
            annotations=immu.Map(_yield_annotations(node)),
        )


class XMLPrivateDimension(models.Dimension):
    tag = "Dimension"

    @classmethod
    def parse(cls, node: etree._Element, index: int):
        """Parse a Private <Dimension> XML node."""
        dimension: cls = XMLSharedDimension.parse.__func__(cls, node, index)

        # foreign keys are required in Private Dimensions
        if dimension.foreign_key is None:
            raise MissingXMLAttribute(node.tag, "foreign_key")

        return dimension


class XMLHierarchy(models.Hierarchy):
    tag = "Hierarchy"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <Hierarchy> XML node."""
        node_name = _get_attr(node, "name")

        level_map = OrderedDict(_yield_children_nodes(node, XMLLevel))
        if len(level_map) == 0:
            raise MissingXMLNode(node.tag, node_name, "Level")

        default_pk = ""
        for item in level_map.values():
            default_pk = item.key_column

        return cls(
            name=node_name,
            primary_key=node.get("primary_key", default_pk),
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
            table=_find_table_ref(node),
            level_map=level_map,
            default_member=cls._parse_default_member(node),
            annotations=immu.Map(_yield_annotations(node)),
        )

    @staticmethod
    def _parse_default_member(node: etree._Element):
        items: List[str] = node.get("default_member", "").split(".", maxsplit=1)
        return tuple(items) if len(items) == 2 else None


class XMLLevel(models.Level):
    tag = "Level"

    @classmethod
    def parse(cls, node: etree._Element, index: int):
        """Parse a <Level> XML node."""
        key_type = node.get("key_type")

        return cls(
            name=_get_attr(node, "name"),
            depth=index + 1,
            key_column=_get_attr(node, "key_column"),
            key_type=MemberType.from_str(key_type),
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
            name_column_map=immu.Map(_yield_locale_pairs(node, "name_column")),
            property_map=OrderedDict(_yield_children_nodes(node, XMLProperty)),
            annotations=immu.Map(_yield_annotations(node)),
        )


class XMLProperty(models.Property):
    tag = "Property"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <Property> XML node."""
        key_type = node.get("key_type")

        keycol_map = immu.Map(_yield_locale_pairs(node, "key_column"))
        if len(keycol_map) == 0:
            raise MissingXMLAttribute(node.tag, "key_column")

        return cls(
            name=_get_attr(node, "name"),
            annotations=immu.Map(_yield_annotations(node)),
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
            key_column_map=keycol_map,
            key_type=MemberType.from_str(key_type),
        )


class XMLMeasure(models.Measure):
    tag = "Measure"

    @classmethod
    def parse(cls, node: etree._Element, _: int):
        """Parse a <Measure> XML node."""
        submeasures = (
            (item.name, item)
            for item in (
                models.SubMeasure(
                    name=_get_attr(item, "name"),
                    aggregator=cls._get_aggregator(item),
                )
                for item in node.iterchildren("Submeasure")
            )
        )
        return cls(
            name=_get_attr(node, "name"),
            key_column=_get_attr(node, "key_column"),
            aggregator=cls._get_aggregator(node),
            annotations=immu.Map(_yield_annotations(node)),
            captions=immu.Map(_yield_locale_pairs(node, "caption")),
            submeasures=immu.Map(submeasures),
        )

    @staticmethod
    def _get_aggregator(mea_node: etree._Element) -> Aggregator:
        """
        Raises:
            :class:`MissingXMLAttribute` --
                If the node doesn't have an `aggregator` attribute or an
                `<Agregation>` child node.

            :class:`InvalidXMLAttributeValue` --
                If the aggregator defined for this node has an unexpected value.
        """

        agg_node = mea_node.find("Aggregation")

        # if there's an <Aggregation> node, get its `type`
        # else get the `<Measure>`'s `aggregator` attribute
        node, attr = (mea_node, "aggregator") if agg_node is None else (agg_node, "type")
        value = _get_attr(node, attr)

        try:
            agg_type = AggregatorType.from_str(value)
        except ValueError:
            node_name = _get_attr(mea_node, "name")
            raise InvalidXMLAttributeValue(node.tag, node_name, attr, value)
        else:
            agg_cls = Aggregator.from_enum(agg_type)
            return agg_cls.new(node.attrib)


def _find_table_ref(node: etree._Element):
    table_node = next(node.iterchildren("InlineTable", "Table", "TableUsage"), None)

    if table_node is None:
        return None
    elif table_node.tag == "InlineTable":
        return XMLInlineTable.parse(table_node, 0)
    elif table_node.tag == "Table":
        return XMLTable.parse(table_node, 0)
    elif table_node.tag == "TableUsage":
        return _get_attr(table_node, "source")

    raise MissingXMLNode(node.tag, _get_attr(node, "name"), "Table")


def _get_attr(node: etree._Element, attr: str) -> str:
    try:
        value = node.attrib[attr]
    except KeyError:
        raise MissingXMLAttribute(node.tag, attr)
    else:
        return value


def _yield_annotations(node: etree._Element) -> Iterable[Tuple[str, Optional[str]]]:
    return (
        (_get_attr(item, "name"), item.text)
        for item in node.iterchildren("Annotation")
    )


def _yield_children_nodes(
    node: etree._Element,
    *children: Type[AnyXMLEntity],
    attr: str = "name",
) -> Generator[Tuple[str, AnyXMLEntity], None, None]:
    tags = (item.tag for item in children)
    parsers = {item.tag: item.parse for item in children}
    for index, item in enumerate(node.iterchildren(*tags)):
        reducer = parsers[item.tag]
        yield _get_attr(item, attr), reducer(item, index)


def _yield_locale_pairs(node: etree._Element,
                        attribute: str) -> Generator[Tuple[str, str], None, None]:
    attr_value = node.get(attribute)
    if attr_value is not None:
        yield ("xx", attr_value)

    for child_node in node.iterchildren("LocalizedAttr"):
        child_attr = _get_attr(child_node, "attr")
        if child_attr != attribute:
            continue

        child_value = child_node.get("value", child_node.text)
        if child_value is not None:
            yield (_get_attr(child_node, "locale"), child_value)


def _parse_pathlib_path(path: Path, parser: etree.XMLParser) -> XMLSchema:
    """Parses an XML schema from the content of a specific pathlib.Path instance.

    This function is able to parse a single file, or all files in a directory.
    """
    if not path.exists():
        raise FileNotFoundError("XML source: Path {} does not exist".format(path))

    def read_xml_path(path: Path) -> XMLSchema:
        with path.open("r") as fileio:
            tree = etree.parse(fileio, parser)
        root = tree.getroot()
        return XMLSchema.parse(root)

    # If path is directory, load all XMLs and combine them
    if path.is_dir():
        schemas = (read_xml_path(item)
                  for item in path.glob("**/*.xml") if item.is_file())
        return XMLSchema.join(*schemas)

    # If path is file, load and parse it
    if path.is_file():
        return read_xml_path(path)

    raise ValueError("XML source: Path can't be interpreted")


def parse_xml_schema(source: Union[str, Path, TextIO]) -> XMLSchema:
    """Attempts to parse an object into a XMLSchema.

    This function accepts:
    - An URL (as a :class:`str`)
    - A local path (as a :class:`str` or :class:`pathlib.Path`) to a XML file,
      or a directory containing XML files
    - A raw XML :class:`str`
    - A not-binary read-only :class:`TextIO` instance for a file-like object
    """
    parser = etree.XMLParser(encoding="utf-8",
                             remove_blank_text=True,
                             remove_comments=True)

    # if argument is string...
    if isinstance(source, str):
        source = source.strip()

        # Check if argument is a URL and fetch the file
        if source.startswith(("http://", "https://", "ftp://")):
            response = httpx.get(source)
            response.raise_for_status()

            root = etree.fromstring(response.text, parser)
            return XMLSchema.parse(root)

        # Check if argument is a path and load the file(s)
        elif source.endswith((".xml", "/", "\\")):
            path = Path(source).resolve()
            return _parse_pathlib_path(path, parser)

        # Check if argument is a raw XML string
        elif source.startswith("<Schema "):
            root = etree.fromstring(source, parser)
            return XMLSchema.parse(root)

        raise ValueError("XML source: Value can't be recognized")

    # if argument is a pathlib.Path, open it and parse contents
    elif isinstance(source, Path):
        path = source.resolve()
        return _parse_pathlib_path(path, parser)

    # if argument is not a string, attempt to use it like a file-like object
    else:
        tree = etree.parse(source, parser)
        root = tree.getroot()
        return XMLSchema.parse(root)
