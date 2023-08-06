import logging

from asyncpg import InvalidCatalogNameError
from sqlalchemy.ext.asyncio import create_async_engine

from ..api import DAPSession
from .base import Arguments, CommandRegistrar


class DatabaseConnectionError(RuntimeError):
    pass


def connect_to_db(connection_string: str):
    engine = create_async_engine(connection_string)
    return engine.connect()


class AbstractDbCommandRegistrar(CommandRegistrar):
    async def _before_execute(self, args: Arguments, session: DAPSession) -> None:
        try:
            logging.debug(f"Checking connection to {args.connection_string}")
            async with connect_to_db(args.connection_string):
                # simply open and close connection to check validity
                pass
        except (InvalidCatalogNameError, OSError) as e:
            # in this case either host/port or database name is invalid
            raise DatabaseConnectionError(f"database connection error: {e}")
