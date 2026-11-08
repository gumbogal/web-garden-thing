"""Public package entry points for the web garden generator."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = ["LeafSpec", "generate_leaf", "main"]

if TYPE_CHECKING:
    from .generators.leaf_generator import LeafSpec, generate_leaf


def __getattr__(name: str) -> Any:
    if name in {"LeafSpec", "generate_leaf"}:
        generator = import_module(".leaf_generator", __name__)
        return getattr(generator, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def main() -> None:
    import_module(".leaf_generator", __name__)
