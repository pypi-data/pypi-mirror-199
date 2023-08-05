import logging
from pathlib import Path
from typing import Union, overload

import httpx
from typing_extensions import Literal

from tesseract_olap.backend import Backend
from tesseract_olap.query import (DataQuery, DataRequest, DataResult,
                                  MembersQuery, MembersRequest, MembersResult)
from tesseract_olap.query.exceptions import InvalidQuery
from tesseract_olap.schema import Schema, SchemaTraverser, parse_xml_schema

from .exceptions import UnknownBackendError, UnknownSchemaError

logger = logging.getLogger("tesseract_olap.server")


class OlapServer:
    """Main server class.

    This object manages the connection with the backend database and the schema
    instance containing the database references, to enable make queries against
    them.
    """
    schema: "SchemaTraverser"
    backend: "Backend"

    def __init__(self,
                 backend: Union[str, "Backend"],
                 schema: Union[str, "Path", "Schema"]):
        self.backend = (
            backend
            if isinstance(backend, Backend) else
            _setup_backend(backend)
        )

        self.schema = SchemaTraverser(
            schema
            if isinstance(schema, Schema) else
            _setup_schema(schema)
        )

    @property
    def raw_schema(self):
        """Retrieves the raw Schema instance used by this server."""
        return self.schema.schema

    async def connect(self):
        """Initializes the connection to the backend server."""
        self.schema.validate()
        await self.backend.connect()
        await self.backend.validate_schema(self.schema)

    async def disconnect(self):
        """Terminates cleanly the currently active connections."""
        self.backend.close()
        await self.backend.wait_closed()

    async def ping(self) -> bool:
        """Performs a ping call to the backend server.
        A succesful call should make this function return :bool:`True`.
        """
        try:
            return await self.backend.ping()
        except IndexError:
            return False

    @overload
    async def execute(self, request: DataRequest, **kwargs) -> DataResult:
        ...
    @overload
    async def execute(self, request: MembersRequest, **kwargs) -> MembersResult:
        ...
    async def execute(
        self,
        request: Union[DataRequest, MembersRequest],
        **kwargs
    ) -> Union[DataResult, MembersResult]:
        """
        If the request is an instance of :class:`DataRequest`, gets the aggregated
        data from the backend and wraps it in a :class:`DataResult` object.
        If the request is an instance of :class:`MembersRequest`, gets the list
        of categories associated to the requested level and wraps the result in
        a :class:`MembersResult` object.
        """
        # The `first` pattern forces the driver to raise any errors in the body
        # of this function, so this can be safely wrapped in a try/except block.

        if isinstance(request, MembersRequest):
            query = MembersQuery.from_request(self.schema, request)
            data = self.backend.execute(query, **kwargs)
            try:
                first = await data.__anext__()
            except StopAsyncIteration:
                first = None
            return MembersResult(first, data, request)

        if isinstance(request, DataRequest):
            query = DataQuery.from_request(self.schema, request)
            data = self.backend.execute(query, **kwargs)
            try:
                first = await data.__anext__()
            except StopAsyncIteration:
                first = None
            sources = query.get_sources()
            return DataResult(first, data, sources, request)

        raise InvalidQuery(
            "OlapServer only accepts instances of DataRequest or MembersRequest"
        )


def _setup_backend(connection: str):
    """Generates a new instance of a backend bundled in this package, or raises
    an error if no one is compatible, with a provided connection string.
    """
    if connection.startswith("clickhouse:") or connection.startswith("clickhouses:"):
        from tesseract_olap.backend.clickhouse import ClickhouseBackend
        return ClickhouseBackend(connection)

    raise UnknownBackendError(connection)


def _setup_schema(source: Union[str, Path]) -> "Schema":
    """Generates a new Schema instance from a string source.

    The source can be a path to a local file, an URL to an external schema file,
    or the text content of a schema file to be parsed.
    Raises a :class:`ValueError` instance if the source can't be recognized as
    either of these.
    """
    # if argument is string...
    if isinstance(source, str):
        source = source.strip()

        # Check if argument is a URL and fetch the file
        if source.startswith(("http:", "https:", "ftp:")):
            logger.debug("Retrieving schema from URL: %s", source)
            response = httpx.get(source)
            response.raise_for_status()
            text = response.text.strip()
            kind = "xml" if text.startswith("<") else "json"
            return _parse_file_contents(text, kind)

        # Check if argument is a raw XML string
        if source.startswith("<"):
            logger.debug("Parsing schema from XML string")
            return _parse_file_contents(source, "xml")

        # Check if argument is a raw JSON string
        if source.startswith("{"):
            logger.debug("Parsing schema from JSON string")
            return _parse_file_contents(source, "json")

        # Assume source is a filesystem path
        # Transform it and let next block handle it
        source = Path(source)

    # if argument is a pathlib.Path, open it and parse contents
    if isinstance(source, Path):
        return _parse_pathlib_path(source.resolve())

    raise ValueError("Schema source can't be recognized as URL, file or raw string")


def _parse_file_contents(source: str, kind: Literal["json", "xml"]) -> "Schema":
    """Starting from a string with the schema contents, is JSON or XML format,
    this function returns the parsed results of that content into a
    :class:`Schema` instance.

    This is useful when the Schema is obtained from a remote location.
    """

    if kind == "json":
        raise NotImplementedError("Parsing JSON files is not implemented yet")

    if kind == "xml":
        return parse_xml_schema(source)

    raise UnknownSchemaError(kind)


def _parse_pathlib_path(path: Path) -> "Schema":
    """Checks if the path exists, is an accepted file format, opens it, and
    parses its contents into a :class:`Schema` instance.
    """
    if not path.exists():
        raise FileNotFoundError(path)

    elif path.is_file():
        logger.debug("Parsing schema from local file: %s", path)

    elif path.is_dir():
        logger.debug("Parsing schema from local directory: %s", path)

    return parse_xml_schema(path)
