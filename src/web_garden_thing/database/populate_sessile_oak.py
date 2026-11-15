
"""Add sessile oak to the botanical database."""

from web_garden_thing.database.connection import get_connection

SPECIES_ID = "quercus_petraea"

TAXONOMY = [
    ("Plantae", "kingdom"),
    ("Streptophyta", "division"),
    ("Equisetopsida", "class"),
    ("Fagales", "order"),
    ("Fagaceae", "family"),
    ("Quercus", "genus"),
    ("Quercus petraea (Matt.) Liebl.", "species"),
]

SOURCES = [
    {
        "title": "Quercus petraea (Matt.) Liebl.",
        "publisher": "Royal Botanic Gardens, Kew",
        "url": (
            "https://powo.science.kew.org/taxon/"
            "urn:lsid:ipni.org:names:359961-1"
        ),
        "source_type": "Taxonomic reference",
        "accessed_on": "2026-11-15",
    },
    {
        "title": "Sessile Oak (Quercus petraea)",
        "publisher": "Woodland Trust",
        "url": (
            "https://www.woodlandtrust.org.uk/trees-woods-and-wildlife/"
            "british-trees/a-z-of-british-trees/sessile-oak/"
        ),
        "source_type": "Species profile",
        "accessed_on": "2026-11-15",
    },
    {
        "title": "Oak, sessile",
        "publisher": "Woodland Trust",
        "url": (
            "https://naturescalendar.woodlandtrust.org.uk/"
            "what-we-record-and-why/species-we-record/trees/oak-sessile/"
        ),
        "source_type": "Identification reference",
        "accessed_on": "2026-11-15",
    },
]


def populate_sessile_oak() -> None:
    """Insert sessile oak and its associated botanical records."""

    with get_connection() as connection:

        # Insert the taxonomic hierarchy.
        parent_taxon_id = None

        for scientific_name, rank in TAXONOMY:
            connection.execute(
                """
                INSERT INTO taxa (
                    scientific_name,
                    rank,
                    parent_taxon_id
                )
                VALUES (?, ?, ?)
                ON CONFLICT(scientific_name) DO NOTHING
                """,
                (scientific_name, rank, parent_taxon_id),
            )

            taxon = connection.execute(
                """
                SELECT id
                FROM taxa
                WHERE scientific_name = ?
                """,
                (scientific_name,),
            ).fetchone()

            parent_taxon_id = taxon["id"]

        # Insert the species.
        connection.execute(
            """
            INSERT INTO species (
                id,
                taxon_id,
                growth_form,
                description
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                taxon_id = excluded.taxon_id,
                growth_form = excluded.growth_form,
                description = excluded.description
            """,
            (
                SPECIES_ID,
                parent_taxon_id,
                "Deciduous tree",
                (
                    "A native deciduous broadleaf tree, particularly "
                    "associated with western Britain. It has lobed, "
                    "alternate leaves and produces acorns attached "
                    "directly to the twigs."
                ),
            ),
        )

        # Insert the common name.
        connection.execute(
            """
            INSERT INTO common_names (
                species_id,
                name,
                language,
                is_preferred
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(species_id, name, language)
            DO UPDATE SET is_preferred = excluded.is_preferred
            """,
            (SPECIES_ID, "Sessile oak", "en", 1),
        )

        # Associate the species with native broadleaf woodland.
        connection.execute(
            """
            INSERT INTO species_habitats (
                species_id,
                habitat_id,
                notes
            )
            VALUES (?, ?, ?)
            ON CONFLICT(species_id, habitat_id)
            DO UPDATE SET notes = excluded.notes
            """,
            (
                SPECIES_ID,
                "native_broadleaf_woodland",
                (
                    "A native tree found in semi-natural woodland, "
                    "particularly in the north and west of Britain."
                ),
            ),
        )

        # Insert sources and connect them to the species.
        for source in SOURCES:
            connection.execute(
                """
                INSERT INTO sources (
                    title,
                    publisher,
                    url,
                    source_type,
                    accessed_on
                )
                VALUES (
                    :title,
                    :publisher,
                    :url,
                    :source_type,
                    :accessed_on
                )
                ON CONFLICT(url) DO UPDATE SET
                    title = excluded.title,
                    publisher = excluded.publisher,
                    source_type = excluded.source_type,
                    accessed_on = excluded.accessed_on
                """,
                source,
            )

            source_record = connection.execute(
                """
                SELECT id
                FROM sources
                WHERE url = ?
                """,
                (source["url"],),
            ).fetchone()

            connection.execute(
                """
                INSERT INTO species_sources (
                    species_id,
                    source_id,
                    information_type
                )
                VALUES (?, ?, ?)
                ON CONFLICT(
                    species_id,
                    source_id,
                    information_type
                ) DO NOTHING
                """,
                (
                    SPECIES_ID,
                    source_record["id"],
                    source["source_type"],
                ),
            )

    print("Successfully added sessile oak to the database.")


if __name__ == "__main__":
    populate_sessile_oak()
