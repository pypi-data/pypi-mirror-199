from __future__ import annotations

import contextlib
import csv
import io
import logging
import os
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

import pyarrow as pa
import pyarrow.csv

from chalk.features import FeatureConverter
from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import (
    BaseSQLSource,
    TableIngestMixIn,
    UnsupportedEfficientExecutionError,
    validate_dtypes_for_efficient_execution,
)
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine import URL, Connection

try:
    import sqlalchemy as sa
except ImportError:
    sa = None

if sa is None:
    _supported_sqlalchemy_types_for_pa_csv_querying = ()
else:
    _supported_sqlalchemy_types_for_pa_csv_querying = (
        sa.BigInteger,
        sa.Boolean,
        sa.Float,
        sa.Integer,
        sa.String,
        sa.Text,
        sa.DateTime,
        sa.Date,
        sa.SmallInteger,
        sa.BIGINT,
        sa.BOOLEAN,
        sa.CHAR,
        sa.DATETIME,
        sa.FLOAT,
        sa.INTEGER,
        sa.SMALLINT,
        sa.TEXT,
        sa.TIMESTAMP,
        sa.VARCHAR,
    )

_logger = get_logger(__name__)


class PostgreSQLSourceImpl(BaseSQLSource, TableIngestMixIn, SQLSourceWithTableIngestProtocol):
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
    ):
        try:
            import psycopg2
        except ImportError:
            raise missing_dependency_exception("chalkpy[postgresql]")
        del psycopg2  # unused
        self.name = name
        self.host = host or load_integration_variable(integration_name=name, name="PGHOST")
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(integration_name=name, name="PGPORT", parser=int)
        )
        self.db = db or load_integration_variable(integration_name=name, name="PGDATABASE")
        self.user = user or load_integration_variable(integration_name=name, name="PGUSER")
        self.password = password or load_integration_variable(integration_name=name, name="PGPASSWORD")
        self.ingested_tables: Dict[str, Any] = {}
        BaseSQLSource.__init__(self, name=name)

    def engine_args(self) -> Dict[str, Any]:
        default = dict(
            pool_size=20,
            max_overflow=60,
            pool_pre_ping=env_var_bool("USE_CLIENT_POOL_PRE_PING"),
            # Trying to fix mysterious dead connection issue
            connect_args={
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
        if self.name is not None:
            additional = self.load_env_engine_args(name=self.name)
            default.update(additional)
        return default

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
        connection: Optional[Connection] = None,
    ) -> pa.Table:
        import psycopg2.sql
        from sqlalchemy.sql import Select

        if env_var_bool("CHALK_FORCE_SQLALCHEMY_QUERY_EXECUTION"):
            raise UnsupportedEfficientExecutionError(
                (
                    f"The SQL statement will be executed into SQLAlchemy objects, as the environment "
                    "variable 'CHALK_FORCE_SQLALCHEMY_QUERY_EXECUTION' is set. Unset this variable to execute "
                    "the query directly into a PyArrow table."
                ),
                log_level=logging.DEBUG,
            )

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(
                finalized_query.query, _supported_sqlalchemy_types_for_pa_csv_querying
            )
        stmt, positional_params, named_params = self.compile_query(finalized_query, paramstyle="named")
        assert len(positional_params) == 0, "should not have any positional params"
        # Forcing quote so the unquoted empty string will represent null values
        stmt = f"COPY ({stmt}) TO STDOUT (FORMAT CSV, HEADER true, FORCE_QUOTE *, ESCAPE '\\')"
        # Convert the param style to python3-style {}, which is what psycopg2.sql.SQL.format expects
        for named_param in named_params:
            stmt = stmt.replace(f":{named_param}", ("{" f"{named_param}" "}"))
        formatted_stmt = psycopg2.sql.SQL(stmt).format(
            **{k: psycopg2.sql.Literal(v) for (k, v) in named_params.items()}
        )
        with self.get_engine().connect() if connection is None else contextlib.nullcontext(connection) as cnx:
            dbapi = cnx.connection
            with dbapi.cursor() as cursor:
                buffer = io.BytesIO()
                cursor.copy_expert(formatted_stmt, buffer)
        buffer.seek(0)
        # Peek the column names
        first_line = buffer.readline()
        column_names = list(
            csv.reader([first_line.decode("utf8")], escapechar="\\", doublequote=False, quoting=csv.QUOTE_ALL)
        )[0]
        buffer.seek(0)
        converters = columns_to_converters(column_names)

        schema = pa.schema([pa.field(k, v.pyarrow_dtype) for (k, v) in converters.items()])

        return pyarrow.csv.read_csv(
            buffer,
            parse_options=pyarrow.csv.ParseOptions(
                newlines_in_values=True,
                escape_char="\\",
                double_quote=False,
            ),
            convert_options=pyarrow.csv.ConvertOptions(
                true_values=["t"],
                false_values=["f"],
                strings_can_be_null=True,
                quoted_strings_can_be_null=False,
                column_types=schema,
            ),
        )
