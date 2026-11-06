"""Public package entry points for the web garden generator."""

from .leaf_generator import LeafSpec, generate_leaf

__all__ = ["LeafSpec", "generate_leaf", "main"]


def main() -> None:
    generate_leaf()
