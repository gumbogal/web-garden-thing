import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StemSpec:
    """Parameters controlling stem geometry."""

    height: float = 2.5
    base_radius: float = 0.045
    tip_radius: float = 0.018
    bend_x: float = 0.15
    bend_y: float = 0.05
    segments: int = 12
    sides: int = 6

    def __post_init__(self) -> None:
        """Validate stem dimensions and mesh resolution."""
        dimensions = {
            "height": self.height,
            "base_radius": self.base_radius,
            "tip_radius": self.tip_radius,
            "bend_x": self.bend_x,
            "bend_y": self.bend_y,
        }

        for name, value in dimensions.items():
            if not math.isfinite(value):
                raise ValueError(f"{name} must be a finite number.")

        for name in ("height", "base_radius", "tip_radius"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be greater than zero.")

        if self.segments < 1:
            raise ValueError("Segments must be at least 1.")

        if self.sides < 3:
            raise ValueError("Sides must be at least 3.")
