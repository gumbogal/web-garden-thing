
"""Create the Web Garden Thing database schema."""

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "web_garden_thing.db"


SCHEMA = """
CREATE TABLE IF NOT EXISTS taxa (
    id INTEGER PRIMARY KEY,
    scientific_name TEXT NOT NULL UNIQUE,
    rank TEXT NOT NULL,
    parent_taxon_id INTEGER,
    authority TEXT,

    FOREIGN KEY (parent_taxon_id)
        REFERENCES taxa(id),

    CHECK (
        rank IN (
            'kingdom',
            'division',
            'class',
            'order',
            'family',
            'genus',
            'species'
        )
    )
);


CREATE TABLE IF NOT EXISTS species (
    id TEXT PRIMARY KEY,
    taxon_id INTEGER NOT NULL UNIQUE,
    growth_form TEXT,
    description TEXT,

    FOREIGN KEY (taxon_id)
        REFERENCES taxa(id)
);


CREATE TABLE IF NOT EXISTS common_names (
    id INTEGER PRIMARY KEY,
    species_id TEXT NOT NULL,
    name TEXT NOT NULL,
    language TEXT NOT NULL DEFAULT 'en',
    is_preferred INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (species_id)
        REFERENCES species(id)
        ON DELETE CASCADE,

    UNIQUE (species_id, name, language),

    CHECK (is_preferred IN (0, 1))
);


CREATE TABLE IF NOT EXISTS habitats (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);


CREATE TABLE IF NOT EXISTS species_habitats (
    species_id TEXT NOT NULL,
    habitat_id TEXT NOT NULL,
    notes TEXT,

    PRIMARY KEY (species_id, habitat_id),

    FOREIGN KEY (species_id)
        REFERENCES species(id)
        ON DELETE CASCADE,

    FOREIGN KEY (habitat_id)
        REFERENCES habitats(id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    publisher TEXT,
    url TEXT NOT NULL UNIQUE,
    source_type TEXT,
    accessed_on TEXT,
    licence TEXT,
    notes TEXT
);


CREATE TABLE IF NOT EXISTS species_sources (
    species_id TEXT NOT NULL,
    source_id INTEGER NOT NULL,
    information_type TEXT NOT NULL,
    notes TEXT,

    PRIMARY KEY (
        species_id,
        source_id,
        information_type
    ),

    FOREIGN KEY (species_id)
        REFERENCES species(id)
        ON DELETE CASCADE,

    FOREIGN KEY (source_id)
        REFERENCES sources(id)
        ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS idx_taxa_parent
    ON taxa(parent_taxon_id);

CREATE INDEX IF NOT EXISTS idx_common_names_name
    ON common_names(name);

CREATE INDEX IF NOT EXISTS idx_species_habitats_habitat
    ON species_habitats(habitat_id);

CREATE INDEX IF NOT EXISTS idx_species_sources_source
    ON species_sources(source_id);
"""


def create_schema() -> None:
    """Create all database tables and indexes."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA)
        connection.execute("PRAGMA user_version = 1")

    print("Database schema created successfully.")
    print(f"Database location: {DATABASE_PATH}")


if __name__ == "__main__":
    create_schema()
