"""Inspect the Web Garden Thing database."""

import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "web_garden_thing.db"


def inspect_database() -> None:
    """Print the names of tables in the project database."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
            """
        ).fetchall()

    print("Database tables:")
    for (table_name,) in tables:
        print(f"- {table_name}")


if __name__ == "__main__":
    inspect_database()
