"""Species profile models and database loading."""

from dataclasses import dataclass
from typing import Any

from web_garden_thing.database.species import get_species


@dataclass(frozen=True, slots=True)
class Taxon:
    """A taxonomic classification of a species."""

    scientific_name: str
    rank: str
    authority: str


@dataclass(frozen=True, slots=True)
class CommonName:
    """A common name associated with a species."""

    name: str
    language: str
    is_preferred: bool


@dataclass(frozen=True, slots=True)
class Habitat:
    """A habitat associated with a species."""

    id: str
    name: str
    description: str | None
    notes: str | None


@dataclass(frozen=True, slots=True)
class Source:
    """A reference associated with a species."""

    id: int
    title: str
    publisher: str | None
    url: str
    source_type: str | None
    information_type: str
    accessed_on: str | None
    licence: str | None
    notes: str | None
    relationship_notes: str | None


@dataclass(frozen=True, slots=True)
class SpeciesProfile:
    """A complete botanical profile of a species."""

    id: str
    scientific_name: str
    rank: str
    authority: str | None
    growth_form: str | None
    description: str | None

    taxonomy: tuple[Taxon, ...]
    common_names: tuple[CommonName, ...]
    habitats: tuple[Habitat, ...]
    sources: tuple[Source, ...]

    @classmethod
    def from_record(
        cls,
        record: dict[str, Any],
    ) -> SpeciesProfile:
        """Create a species profile instance from a database record."""

        return cls(
            id=record["id"],
            scientific_name=record["scientific_name"],
            rank=record["rank"],
            authority=record.get("authority"),
            growth_form=record.get("growth_form"),
            description=record.get("description"),
            taxonomy=tuple(Taxon(**item) for item in record["taxonomy"]),
            common_names=tuple(
                CommonName(
                    name=item["name"],
                    language=item["language"],
                    is_preferred=bool(item["is_preferred"]),
                )
                for item in record["common_names"]
            ),
            habitats=tuple(Habitat(**item) for item in record["habitats"]),
            sources=tuple(Source(**item) for item in record["sources"]),
        )


def load_species_profile(
    species_id: str,
) -> SpeciesProfile | None:
    """Load a species profile using its database identifier."""
    record = get_species(species_id)

    if record is None:
        return None

    return SpeciesProfile.from_record(record)
