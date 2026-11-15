"""Database connection utilities."""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
database_path = project_root / "data" / "web_garden_thing.db"

@contextmanager
def get_connection() -> Generator[sqlite3.Connection]:
    """Open and safely close a database connection."""

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row  # Enable named column access
    connection.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key support

    try:
        with connection:
            yield connection
    finally:
        connection.close()