# Web Garden Thing

This project generates a stylized leaf mesh in Blender from a small Python module.

## Usage

Run the generator from Blender's Scripting workspace or call the package entry point from a Python environment with Blender available:

```python
from web_garden_thing import generate_leaf

generate_leaf()
```

You can also supply a custom configuration:

```python
from web_garden_thing import LeafSpec, generate_leaf

spec = LeafSpec(length=2.4, width=0.75, rows=11, columns=6)
generate_leaf(spec)
```

The generated object is created inside a collection named `Plant Generator` and includes a procedural leaf mesh with a central midrib and secondary veins.
