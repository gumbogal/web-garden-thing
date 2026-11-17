from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LeafArrangementSpec:
    """Parameters controlling leaf placement and distribution."""

    count: int = 6
    height_min: float = 0.35
    height_max: float = 2.0
    golden_angle: float = 137.5
    angle_offset: float = 0.0
    angle_variation: float = 5.0
    elevation_min: float = -8.0
    elevation_max: float = 25.0
    elevation_variation: float = 4.0
    scale_min: float = 0.75
    scale_max: float = 1.0
