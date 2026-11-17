import sys
from pathlib import Path

# Add the src directory to Python's import path.
src_path = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the plant generator.
from web_garden_thing.generators.leaf_generator import generate_leaf  # noqa: E402

generate_leaf()
