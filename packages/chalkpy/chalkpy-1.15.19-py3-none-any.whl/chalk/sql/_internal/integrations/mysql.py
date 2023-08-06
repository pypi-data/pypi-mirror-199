from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, TableIngestMixIn
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class MySQLSourceImpl(BaseSQLSource, TableIngestMixIn, SQLSourceWithTableIngestProtocol):
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
            import pymysql
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[mysql]")
        del pymysql
        self.name = name
        self.host = host or load_integration_variable(name="MYSQL_HOST", integration_name=name)
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(name="MYSQL_TCP_PORT", integration_name=name, parser=int)
        )
        self.db = db or load_integration_variable(name="MYSQL_DATABASE", integration_name=name)
        self.user = user or load_integration_variable(name="MYSQL_USER", integration_name=name)
        self.password = password or load_integration_variable(name="MYSQL_PWD", integration_name=name)
        self.ingested_tables: Dict[str, Any] = {}
        BaseSQLSource.__init__(self, name=name)

    def engine_args(self) -> Dict[str, Any]:
        default = dict(
            pool_size=20,
            max_overflow=60,
            pool_pre_ping=True,
        )
        if self.name is not None:
            additional = self.load_env_engine_args(name=self.name)
            default.update(additional)
        return default

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="mysql+pymysql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )
