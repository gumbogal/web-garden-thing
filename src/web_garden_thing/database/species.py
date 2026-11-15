"""Retrieve botanical species and their associated information from the database."""

from typing import Any

from web_garden_thing.database.connection import get_connection


def get_species(species_id: str) -> dict[str, Any] | None:
    """Retrieve a species and its associated information from the database.

    Args:
        species_id (str): The unique identifier of the species to retrieve.

    Returns:
        A dictionary containing the species and its associated
        information, or None if the species does not exist.

        dict[str, Any] | None: The species information if found, otherwise None.
    """

    with get_connection() as connection:
        #Retrieve the main species record.
        species = connection.execute(
            """
            SELECT
                species.id,
                species.growth_form,
                species.description,
                taxa.scientific_name,
                taxa.rank,
                taxa.authority,
                species.taxon_id
            FROM species
            JOIN taxa ON species.taxon_id = taxa.id
            WHERE species.id = ?
            """,
            (species_id,),
        ).fetchone()

        if species is None:
            return None

        result = dict(species)

        # Retrieve the complete taxonomic hierarchy.
        taxonomy = connection.execute(
            """
            WITH RECURSIVE taxonomy (
                id,
                scientific_name,
                rank,
                authority,
                parent_taxon_id,
                depth
            ) AS (
                SELECT
                    id,
                    scientific_name,
                    rank,
                    authority,
                    parent_taxon_id,
                    0
                FROM taxa
                WHERE id = ?

                UNION ALL

                SELECT
                    parent.id,
                    parent.scientific_name,
                    parent.rank,
                    parent.authority,
                    parent.parent_taxon_id,
                    child.depth + 1
                FROM taxa AS parent
                JOIN taxonomy AS child
                    ON child.parent_taxon_id = parent.id
            )
            SELECT
                scientific_name,
                rank,
                authority
            FROM taxonomy
            ORDER BY depth DESC
            """,
            (result["taxon_id"],),
        ).fetchall()

        result["taxonomy"] = [dict(row) for row in taxonomy]

        # Retrieve common names.
        common_names = connection.execute(
            """
            SELECT
                name,
                language,
                is_preferred
            FROM common_names
            WHERE species_id = ?
            ORDER BY is_preferred DESC, name
            """,
            (species_id,),
        ).fetchall()

        result["common_names"] = [
            dict(row) for row in common_names
        ]

        # Retrieve associates habitats.
        habitats = connection.execute(
            """
            SELECT
                habitats.id,
                habitats.name,
                habitats.description,
                species_habitats.notes
            FROM species_habitats
            JOIN habitats 
                ON species_habitats.habitat_id = habitats.id
            WHERE species_habitats.species_id = ?
            ORDER BY habitats.name
            """,
            (species_id,),
        ).fetchall()

        result["habitats"] = [
            dict(row) for row in habitats
        ]

        # Retrieve associated sources.
        sources = connection.execute(
            """
            SELECT
                sources.id,
                sources.title,
                sources.publisher,
                sources.url,
                sources.source_type,
                sources.accessed_on,
                sources.licence,
                species_sources.notes,
                species_sources.information_type,
                species_sources.notes AS relationship_notes
            FROM species_sources
            JOIN sources 
                ON species_sources.source_id = sources.id
            WHERE species_sources.species_id = ?
            ORDER BY sources.title
            """,
            (species_id,),
        ).fetchall()

        result["sources"] = [
            dict(row) for row in sources
        ]

        return result