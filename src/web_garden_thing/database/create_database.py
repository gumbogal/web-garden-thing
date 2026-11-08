"""Create the Web Garden Thing SQLite database."""

import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
db_path = project_root / "data" / "web_garden_thing.db"

def create_database() -> None:
    """Create the database if it does not already exist."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        print("Database connection successful")

    print(f"Database created at {db_path}")


if __name__ == "__main__":
    create_database()