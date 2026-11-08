"""Inspect the Web Garden Thing database."""

import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
db_path = project_root / "data" / "web_garden_thing.db"

def inspect_database() -> None:
    with sqlite3.connect(db_path) as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;"""
        ).fetchall()
    print("Database tables:")
    for (table_name,) in tables:
        print(f"- {table_name}")

if __name__ == "__main__":
    inspect_database()