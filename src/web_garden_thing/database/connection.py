"""Database connection utilities."""

import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
database_path = project_root / "data" / "web_garden_thing.db"

def get_connection() -> sqlite3.Connection:
    """Open a connection to the Web Garden Thing database."""

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row  # Enable named column access
    connection.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key support

    return connection