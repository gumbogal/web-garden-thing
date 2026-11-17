"""Tests for species data retrieval and profile conversion."""

import sqlite3
import unittest
from collections.abc import Generator
from contextlib import contextmanager
from unittest.mock import patch

from web_garden_thing.database.create_schema import SCHEMA
from web_garden_thing.species_profile import load_species_profile


@contextmanager
def connection_with_source_notes() -> Generator[sqlite3.Connection, None, None]:
    """Provide an isolated database with different source and link notes."""
    connection = sqlite3.connect(":memory:")
    try:
        connection.row_factory = sqlite3.Row
        connection.executescript(SCHEMA)
        connection.execute(
            """
            INSERT INTO taxa (id, scientific_name, rank)
            VALUES (1, 'Quercus robur', 'species')
            """
        )
        connection.execute("INSERT INTO species (id, taxon_id) VALUES ('oak', 1)")
        connection.execute(
            """
            INSERT INTO sources (id, title, url, notes)
            VALUES (1, 'Reference', 'https://example.test/oak', 'Source note')
            """
        )
        connection.execute(
            """
            INSERT INTO species_sources (
                species_id,
                source_id,
                information_type,
                notes
            )
            VALUES ('oak', 1, 'Taxonomy', 'Relationship note')
            """
        )
        yield connection
    finally:
        connection.close()


class SpeciesProfileTests(unittest.TestCase):
    def test_source_and_relationship_notes_are_loaded_separately(self) -> None:
        with patch(
            "web_garden_thing.database.species.get_connection",
            new=connection_with_source_notes,
        ):
            profile = load_species_profile("oak")

        if profile is None:
            self.fail("Expected the seeded species profile to be returned")

        source = profile.sources[0]
        self.assertEqual(source.notes, "Source note")
        self.assertEqual(source.relationship_notes, "Relationship note")


if __name__ == "__main__":
    unittest.main()
