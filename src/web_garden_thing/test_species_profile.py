"""Test the botanical species profile."""

from web_garden_thing.species_profile import load_species_profile


def main() -> None:
    profile = load_species_profile("quercus_petraea")

    if profile is None:
        raise RuntimeError("Species profile could not be loaded.")

    print(f"Species: {profile.scientific_name}")
    print(f"Growth form: {profile.growth_form}")
    print(f"Taxonomic classification: {len(profile.taxonomy)} ranks")

    print("\nCommon names:")
    for name in profile.common_names:
        preferred = " (preferred)" if name.is_preferred else ""
        print(f" {name.name}{preferred}")

    print("\nHabitats:")
    for habitat in profile.habitats:
        print(f" {habitat.name}")

    print("\nSources")
    for source in profile.sources:
        print(f" {source.title}: {source.url}")


if __name__ == "__main__":
    main()
