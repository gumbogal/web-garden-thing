"""Create the Web Garden Thing SQLite database."""

import sqlite3
from contextlib import closing
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "web_garden_thing.db"


def create_database() -> None:
    """Create the database if it does not already exist."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(DATABASE_PATH)):
        print("Database connection successful")

    print(f"Database created at {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()
