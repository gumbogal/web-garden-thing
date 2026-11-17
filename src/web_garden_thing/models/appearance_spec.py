from dataclasses import dataclass

type Color = tuple[float, float, float, float]


@dataclass(frozen=True, slots=True)
class AppearanceSpec:
    """Colours used by the plant generators."""

    leaf_color: Color = (0.12, 0.32, 0.09, 1.0)
    vein_color: Color = (0.22, 0.42, 0.14, 1.0)
    stem_color: Color = (0.10, 0.25, 0.07, 1.0)
