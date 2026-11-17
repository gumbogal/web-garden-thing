from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LeafSpec:
    """Parameters controlling leaf geometry and venation."""

    length: float = 2.0
    width: float = 0.65
    longitudinal_curve: float = 0.12
    central_ridge: float = 0.10
    base_taper: float = 0.8
    tip_sharpness: float = 1.4
    asymmetry: float = 0.06
    cross_section_cup: float = 0.045

    rows: int = 9
    columns: int = 5

    central_vein_thickness: float = 0.009
    secondary_vein_count: int = 6
    secondary_vein_width: float = 0.008
    secondary_vein_offset: float = 0.002
    secondary_vein_samples: int = 25
    secondary_vein_start: float = 0.18
    secondary_vein_spacing: float = 0.12
    secondary_vein_reach: float = 0.08
