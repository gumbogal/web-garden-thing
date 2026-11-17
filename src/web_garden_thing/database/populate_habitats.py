"""Populate the database with initial woodland habitats."""

from web_garden_thing.database.connection import get_connection

habitats = [
    {
        "id": "native_broadleaf_woodland",
        "name": "Native Broadleaf Woodland",
        "description": (
            "Woodland characterised by native broadleaved trees and "
            "an associated understory of shrubs, ferns and woodland "
            "ground flora."
        ),
    },
    {
        "id": "caledonian_pinewood",
        "name": "Caledonian Pinewood",
        "description": (
            "Native Scottish pine woodland dominated by Scots pine, "
            "with an associated community of shrubs, dwarf shrubs, "
            "mosses, lichens and woodland plants."
        ),
    },
]


def populate_habitats() -> None:
    """Insert the initial habitat records."""

    sql = """
        INSERT INTO habitats (id, name, description)
        VALUES (:id, :name, :description)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            description=excluded.description
    """

    with get_connection() as connection:
        connection.executemany(
            sql,
            habitats,
        )

    print(f"Successfully populated {len(habitats)} habitats.")


if __name__ == "__main__":
    populate_habitats()
