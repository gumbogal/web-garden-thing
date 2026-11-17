from dataclasses import dataclass, field

from .appearance_spec import AppearanceSpec
from .leaf_arrangement_spec import LeafArrangementSpec
from .leaf_spec import LeafSpec
from .stem_spec import StemSpec


@dataclass(frozen=True, slots=True)
class PlantSpec:
    """Complete specification for a generated plant."""

    leaf: LeafSpec = field(default_factory=LeafSpec)
    stem: StemSpec = field(default_factory=StemSpec)
    leaf_arrangement: LeafArrangementSpec = field(default_factory=LeafArrangementSpec)
    appearance: AppearanceSpec = field(default_factory=AppearanceSpec)
