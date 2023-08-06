import argparse
from typing import Any, Callable, Dict, Optional

from sqlalchemy import make_url
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import NoSuchModuleError

from ..arguments import EnvironmentDefault
from .base import ArgumentRegistrar


class DatabaseProtocolError(RuntimeError):
    pass


class DatabaseConnectionStringAction(EnvironmentDefault):
    _dialect_to_driver_mapping: Dict[str, str]

    def __init__(
        self, var: str, *, required=True, default=None, help=None, **kwargs
    ) -> None:
        super().__init__(
            var=var,
            required=required,
            default=default,
            help=help,
            **kwargs,
        )
        self._dialect_to_driver_mapping = {"postgresql": "asyncpg"}

        if self.default is not None:
            self.default = self._modify_url(self.default)

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Any,
        option_string: Optional[str] = None,
    ) -> None:
        modified_url = self._modify_url(values)
        setattr(namespace, self.dest, modified_url)

    def _modify_url(self, original_url: str) -> URL:
        try:
            url = make_url(original_url)
            dialect = url.get_dialect().name
            driver = url.get_dialect().driver
            updated_driver = self._get_driver_for_dialect(dialect)
            if driver != updated_driver:
                url = url.set(drivername=f"{dialect}+{updated_driver}")
            return url
        except NoSuchModuleError as e:
            raise DatabaseProtocolError(f"unknown database protocol: {url.drivername}")

    def _get_driver_for_dialect(self, dialect: str):
        driver: Optional[str] = self._dialect_to_driver_mapping.get(dialect, None)
        if driver is not None:
            return driver
        else:
            raise ValueError(f"SQLAlchemy dialect not supported: {dialect}")


def dbconnstr_environment_default(var: str) -> Callable[..., argparse.Action]:
    "Reads the value of the --connection-string argument from the given environment variable if not supplied as a command-line argument."

    def _dbconnstr_environment_default(**kwargs) -> argparse.Action:
        return DatabaseConnectionStringAction(var, **kwargs)

    return _dbconnstr_environment_default


# Argument registrar classes
class DatabaseConnectionStringArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--connection-string",
            metavar="DBCONNSTR",
            action=dbconnstr_environment_default("DAP_CONNECTION_STRING"),  # type: ignore
            help="The connection string used to connect to the target database.",
        )
