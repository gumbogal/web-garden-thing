"""Database connection utilities."""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "web_garden_thing.db"


@contextmanager
def get_connection() -> Generator[sqlite3.Connection]:
    """Open and safely close a database connection."""

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        with connection:
            yield connection
    finally:
        connection.close()
