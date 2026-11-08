"""Generate a stylized procedural plant in the active Blender scene."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import cast

import bmesh  # type: ignore
import bpy
from mathutils import Vector  # type: ignore

type Color = tuple[float, float, float, float]
type Point3D = tuple[float, float, float]

COLLECTION_NAME = "Plant Generator"


@dataclass(frozen=True, slots=True)
class LeafSpec:
    """Parameters controlling the generated plant and its leaves."""

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

    leaf_count: int = 6
    leaf_height_min: float = 0.35
    leaf_height_max: float = 2.0
    golden_angle: float = 137.5
    leaf_angle_offset: float = 0.0
    leaf_angle_variation: float = 5.0
    leaf_elevation_min: float = -8.0
    leaf_elevation_max: float = 25.0
    leaf_elevation_variation: float = 4.0
    leaf_scale_min: float = 0.75
    leaf_scale_max: float = 1.0

    central_vein_thickness: float = 0.009
    secondary_vein_count: int = 6
    secondary_vein_width: float = 0.008
    secondary_vein_offset: float = 0.002
    secondary_vein_samples: int = 25
    secondary_vein_start: float = 0.18
    secondary_vein_spacing: float = 0.12
    secondary_vein_reach: float = 0.08

    stem_height: float = 2.5
    stem_base_radius: float = 0.045
    stem_tip_radius: float = 0.018
    stem_bend_x: float = 0.15
    stem_bend_y: float = 0.05
    stem_segments: int = 12
    stem_sides: int = 6

    leaf_color: Color = (0.12, 0.32, 0.09, 1.0)
    vein_color: Color = (0.22, 0.42, 0.14, 1.0)
    stem_color: Color = (0.10, 0.25, 0.07, 1.0)


def create_collection(name: str) -> bpy.types.Collection:
    """Create or clear the collection used for the generated plant."""
    collection = bpy.data.collections.get(name)

    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)

    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    return collection


def create_material(name: str, color: Color) -> bpy.types.Material:
    """Create or update a material with the given base color."""
    material = bpy.data.materials.get(name)

    if material is None:
        material = bpy.data.materials.new(name)

    material.diffuse_color = color
    material.use_nodes = True

    principled = material.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs["Base Color"].default_value = color
        principled.inputs["Roughness"].default_value = 0.85

    return material


def leaf_surface(u: float, t: float, spec: LeafSpec) -> Point3D:
    """Return a point on the curved leaf surface for normalized coordinates."""
    if t <= 0.0 or t >= 1.0:
        return (0.0, spec.length * t, 0.0)

    width_profile = math.sin(math.pi * t) ** (1.0 / spec.tip_sharpness)
    width_profile *= spec.base_taper + (1.0 - spec.base_taper) * t

    x = u * spec.width * 0.5 * width_profile
    x += spec.asymmetry * spec.width * math.sin(math.pi * t)

    y = spec.length * t
    ridge = spec.central_ridge * (1.0 - abs(u))
    cup = spec.cross_section_cup * abs(u) ** 1.7
    bend = spec.longitudinal_curve * math.sin(math.pi * t)

    return (x, y, ridge - cup + bend)


def create_leaf_mesh(
    collection: bpy.types.Collection,
    material: bpy.types.Material,
    spec: LeafSpec,
) -> bpy.types.Object:
    """Create the triangulated leaf mesh and store its defining parameters."""
    vertices: list[Point3D] = [(0.0, 0.0, 0.0)]

    for row in range(1, spec.rows + 1):
        t = row / (spec.rows + 1)

        for column in range(spec.columns):
            u = (column / (spec.columns - 1)) * 2.0 - 1.0
            vertices.append(leaf_surface(u, t, spec))

    tip_index = len(vertices)
    vertices.append((0.0, spec.length, 0.0))

    faces: list[tuple[int, ...]] = []

    for column in range(spec.columns - 1):
        faces.append((0, column + 2, column + 1))

    for row in range(spec.rows - 1):
        current = 1 + row * spec.columns
        next_row = current + spec.columns

        for column in range(spec.columns - 1):
            a = current + column
            b = a + 1
            c = next_row + column + 1
            d = next_row + column
            faces.extend(((a, b, c), (a, c, d)))

    last_row = 1 + (spec.rows - 1) * spec.columns
    for column in range(spec.columns - 1):
        faces.append((last_row + column, last_row + column + 1, tip_index))

    mesh = bpy.data.meshes.new("Leaf_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    leaf = bpy.data.objects.new("Leaf_Prototype", mesh)
    collection.objects.link(leaf)
    leaf.data.materials.append(material)

    for polygon in mesh.polygons:
        polygon.use_smooth = False

    leaf["length"] = spec.length
    leaf["width"] = spec.width
    leaf["longitudinal_curve"] = spec.longitudinal_curve
    leaf["central_ridge"] = spec.central_ridge
    leaf["base_taper"] = spec.base_taper
    leaf["tip_sharpness"] = spec.tip_sharpness
    leaf["asymmetry"] = spec.asymmetry
    leaf["cross_section_cup"] = spec.cross_section_cup
    leaf["rows"] = spec.rows
    leaf["columns"] = spec.columns

    return leaf


def sample_leaf_surface(
    target_mesh: bpy.types.Mesh,
    u: float,
    t: float,
    spec: LeafSpec,
) -> tuple[Vector, Vector]:
    """Interpolate a point and normal on the triangulated leaf mesh."""
    t = max(1.0 / (spec.rows + 1), min(t, spec.rows / (spec.rows + 1)))
    u = max(-1.0, min(u, 1.0))

    column_position = (u + 1.0) * 0.5 * (spec.columns - 1)
    column = min(math.floor(column_position), spec.columns - 2)
    x = column_position - column

    row_position = t * (spec.rows + 1)
    row = math.floor(row_position)
    row = max(1, min(row, spec.rows - 1))
    y = row_position - row

    a_index = 1 + (row - 1) * spec.columns + column
    b_index = a_index + 1
    d_index = a_index + spec.columns
    c_index = d_index + 1

    a = Vector(target_mesh.vertices[a_index].co)
    b = Vector(target_mesh.vertices[b_index].co)
    c = Vector(target_mesh.vertices[c_index].co)
    d = Vector(target_mesh.vertices[d_index].co)

    if y <= x:
        point = a * (1.0 - x) + b * (x - y) + c * y
        normal = cast(Vector, (b - a).cross(c - a))
    else:
        point = a * (1.0 - y) + c * x + d * (y - x)
        normal = cast(Vector, (c - a).cross(d - a))

    normal.normalize()
    return point, normal


def normalized_vector(vector: Vector) -> Vector:
    """Normalize a Blender vector, with explicit typing for its stub."""
    return cast(Vector, vector.normalized())


def central_vein_points(leaf_mesh: bpy.types.Mesh, spec: LeafSpec) -> list[Vector]:
    """Return points along the center of the leaf mesh."""
    middle_column = spec.columns // 2
    points = [leaf_mesh.vertices[0].co.copy()]

    for row in range(spec.rows):
        vertex_index = 1 + row * spec.columns + middle_column
        points.append(leaf_mesh.vertices[vertex_index].co.copy())

    points.append(leaf_mesh.vertices[-1].co.copy())
    return points


def create_central_vein(
    points: list[Vector],
    collection: bpy.types.Collection,
    material: bpy.types.Material,
    spec: LeafSpec,
) -> bpy.types.Object:
    """Create the central vein as a beveled curve."""
    curve_data = bpy.data.curves.new("Central_Vein_Curve", "CURVE")
    curve_data.dimensions = "3D"
    curve_data.resolution_u = 1
    curve_data.bevel_depth = spec.central_vein_thickness
    curve_data.bevel_resolution = 0

    spline = curve_data.splines.new("POLY")
    spline.points.add(len(points) - 1)

    for index, point in enumerate(points):
        spline.points[index].co = (*point, 1.0)

    vein = bpy.data.objects.new("Leaf_Central_Vein", curve_data)
    collection.objects.link(vein)
    vein.data.materials.append(material)
    vein["vein_type"] = "central"
    return vein


def deform_leaf_mesh(obj: bpy.types.Object, sweep: float, droop: float, spec: LeafSpec) -> None:
    """Apply a per-leaf sweep and droop deformation to its mesh."""
    for vertex in obj.data.vertices:
        coordinates = vertex.co
        t = max(0.0, min(coordinates.y / spec.length, 1.0))
        profile = math.sin(math.pi * t)

        coordinates.x += sweep * profile
        coordinates.z += droop * profile

    obj.data.update()


def create_secondary_vein_mesh(
    leaf: bpy.types.Object,
    vein_index: int,
    side: int,
    collection: bpy.types.Collection,
    material: bpy.types.Material,
    spec: LeafSpec,
) -> bpy.types.Object:
    """Build a tapered ribbon that follows the triangulated leaf surface."""
    ribbon_vertices: list[Point3D] = []
    ribbon_faces: list[tuple[int, int, int, int]] = []

    start_t = spec.secondary_vein_start + vein_index * spec.secondary_vein_spacing

    for step in range(spec.secondary_vein_samples + 1):
        progress = step / spec.secondary_vein_samples
        u = side * 0.85 * progress
        t = start_t + spec.secondary_vein_reach * progress

        point, normal = sample_leaf_surface(leaf.data, u, t, spec)

        previous_progress = max(0.0, progress - 0.001)
        next_progress = min(1.0, progress + 0.001)

        previous_point, _ = sample_leaf_surface(
            leaf.data,
            side * 0.85 * previous_progress,
            start_t + spec.secondary_vein_reach * previous_progress,
            spec,
        )
        next_point, _ = sample_leaf_surface(
            leaf.data,
            side * 0.85 * next_progress,
            start_t + spec.secondary_vein_reach * next_progress,
            spec,
        )

        tangent = normalized_vector(cast(Vector, next_point - previous_point))
        lateral = normalized_vector(cast(Vector, tangent.cross(normal)))
        width_profile = 0.12 + 0.88 * (1.0 - progress) ** 0.8
        half_width = spec.secondary_vein_width * width_profile * 0.5

        surface_point = point + normal * spec.secondary_vein_offset
        left = surface_point - lateral * half_width
        right = surface_point + lateral * half_width
        ribbon_vertices.extend((tuple(left), tuple(right)))

    for step in range(spec.secondary_vein_samples):
        a = step * 2
        b = a + 1
        c = a + 3
        d = a + 2
        ribbon_faces.append((a, b, c, d))

    vein_mesh = bpy.data.meshes.new(f"Secondary_Vein_Mesh_{vein_index}_{side}")
    vein_mesh.from_pydata(ribbon_vertices, [], ribbon_faces)
    vein_mesh.update()

    vein = bpy.data.objects.new(
        f"Leaf_Secondary_Vein_{vein_index}_{side}",
        vein_mesh,
    )
    collection.objects.link(vein)
    vein.data.materials.append(material)
    vein["vein_type"] = "secondary"
    vein["vein_index"] = vein_index
    vein["vein_side"] = side

    for polygon in vein_mesh.polygons:
        polygon.use_smooth = False

    return vein


def regenerate_central_vein(
    leaf: bpy.types.Object,
    vein: bpy.types.Object,
    spec: LeafSpec,
) -> None:
    """Update a central vein to match a deformed leaf."""
    points = central_vein_points(leaf.data, spec)
    spline = vein.data.splines[0]

    for index, point in enumerate(points):
        spline.points[index].co = (*point, 1.0)


def generate_stem(
    collection: bpy.types.Collection,
    material: bpy.types.Material,
    spec: LeafSpec,
) -> bpy.types.Object:
    """Create a bent, tapered stem mesh."""
    vertices: list[Point3D] = []
    faces: list[tuple[int, ...]] = []

    for segment in range(spec.stem_segments + 1):
        t = segment / spec.stem_segments
        center = Vector((
            spec.stem_bend_x * t**2,
            spec.stem_bend_y * math.sin(math.pi * t),
            spec.stem_height * t,
        ))

        tangent = Vector((
            2.0 * spec.stem_bend_x * t,
            spec.stem_bend_y * math.pi * math.cos(math.pi * t),
            spec.stem_height,
        )).normalized()

        reference = Vector((0.0, 1.0, 0.0))
        axis_u = normalized_vector(cast(Vector, tangent.cross(reference)))
        axis_v = normalized_vector(cast(Vector, tangent.cross(axis_u)))
        radius = spec.stem_base_radius * (1.0 - t) + spec.stem_tip_radius * t

        for side in range(spec.stem_sides):
            angle = (side / spec.stem_sides) * math.tau
            offset = (
                axis_u * math.cos(angle) + axis_v * math.sin(angle)
            ) * radius
            position = cast(Vector, center + offset)
            vertices.append((position.x, position.y, position.z))

    for segment in range(spec.stem_segments):
        for side in range(spec.stem_sides):
            current = segment * spec.stem_sides + side
            next_side = (side + 1) % spec.stem_sides

            a = current
            b = segment * spec.stem_sides + next_side
            c = (segment + 1) * spec.stem_sides + next_side
            d = (segment + 1) * spec.stem_sides + side
            faces.append((a, b, c, d))

    faces.append(tuple(range(spec.stem_sides - 1, -1, -1)))
    tip_start = spec.stem_segments * spec.stem_sides
    faces.append(tuple(tip_start + side for side in range(spec.stem_sides)))

    stem_mesh = bpy.data.meshes.new("Stem_Mesh")
    stem_mesh.from_pydata(vertices, [], faces)
    stem_mesh.update()

    bm = bmesh.new()
    bm.from_mesh(stem_mesh)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(stem_mesh)
    bm.free()
    stem_mesh.update()

    stem = bpy.data.objects.new("Stem_Prototype", stem_mesh)
    collection.objects.link(stem)
    stem.data.materials.append(material)

    for polygon in stem_mesh.polygons:
        polygon.use_smooth = False

    stem["height"] = spec.stem_height
    stem["base_radius"] = spec.stem_base_radius
    stem["tip_radius"] = spec.stem_tip_radius
    stem["bend_x"] = spec.stem_bend_x
    stem["bend_y"] = spec.stem_bend_y
    stem["segments"] = spec.stem_segments
    stem["sides"] = spec.stem_sides
    return stem


def duplicate_leaf_parts(
    leaf_parts: tuple[bpy.types.Object, bpy.types.Object],
    holder: bpy.types.Object,
    collection: bpy.types.Collection,
) -> tuple[bpy.types.Object, bpy.types.Object]:
    """Duplicate the leaf and central vein prototypes under a holder."""
    duplicates: dict[str, bpy.types.Object] = {}

    for original in leaf_parts:
        duplicate = original.copy()
        duplicate.data = original.data.copy()
        collection.objects.link(duplicate)

        duplicate.parent = holder
        duplicate.matrix_parent_inverse.identity()
        duplicate.location = (0.0, 0.0, 0.0)
        duplicate.rotation_euler = (0.0, 0.0, 0.0)
        duplicate.scale = (1.0, 1.0, 1.0)
        duplicates[original.name] = duplicate

    return duplicates["Leaf_Prototype"], duplicates["Leaf_Central_Vein"]


def attach_leaves(
    leaf: bpy.types.Object,
    central_vein: bpy.types.Object,
    collection: bpy.types.Collection,
    vein_material: bpy.types.Material,
    spec: LeafSpec,
) -> None:
    """Duplicate, orient, and deform leaves along the stem."""
    leaf_parts = (leaf, central_vein)

    for index in range(spec.leaf_count):
        progress = index / max(spec.leaf_count - 1, 1)

        angle = (
            math.radians(index * spec.golden_angle)
            + math.radians(spec.leaf_angle_offset)
            + math.radians(math.sin(index * 2.1) * spec.leaf_angle_variation)
        )
        elevation_degrees = (
            spec.leaf_elevation_min
            + (spec.leaf_elevation_max - spec.leaf_elevation_min) * progress
        )
        elevation_degrees += math.sin(index * 1.7) * spec.leaf_elevation_variation
        elevation = math.radians(elevation_degrees)

        direction = Vector((
            math.cos(angle) * math.cos(elevation),
            math.sin(angle) * math.cos(elevation),
            math.sin(elevation),
        )).normalized()

        height = spec.leaf_height_min + (
            spec.leaf_height_max - spec.leaf_height_min
        ) * progress

        holder = bpy.data.objects.new(f"Leaf_Holder_{index + 1}", None)
        collection.objects.link(holder)
        holder.location = Vector((
            spec.stem_bend_x * (height / spec.stem_height) ** 2,
            spec.stem_bend_y * math.sin(math.pi * height / spec.stem_height),
            height,
        ))
        holder.rotation_mode = "QUATERNION"
        holder.rotation_quaternion = direction.to_track_quat("Y", "Z")

        variation = 0.94 + 0.06 * math.sin(index * 2.4)
        scale = (
            spec.leaf_scale_min
            + (spec.leaf_scale_max - spec.leaf_scale_min) * progress
        ) * variation
        holder.scale = (scale, scale, scale)

        leaf_copy, central_copy = duplicate_leaf_parts(
            leaf_parts,
            holder,
            collection,
        )

        sweep = math.sin(index * 2.3) * 0.08
        droop = math.sin(index * 1.7) * 0.12
        deform_leaf_mesh(leaf_copy, sweep, droop, spec)
        regenerate_central_vein(leaf_copy, central_copy, spec)

        for vein_index in range(spec.secondary_vein_count):
            for side in (-1, 1):
                vein = create_secondary_vein_mesh(
                    leaf_copy,
                    vein_index,
                    side,
                    collection,
                    vein_material,
                    spec,
                )
                vein.parent = holder
                vein.matrix_parent_inverse.identity()
                vein.location = (0.0, 0.0, 0.0)
                vein.rotation_euler = (0.0, 0.0, 0.0)
                vein.scale = (1.0, 1.0, 1.0)

    for original in leaf_parts:
        original.hide_set(True)
        original.hide_render = True


def select_generated_plant(
    collection: bpy.types.Collection,
    stem: bpy.types.Object,
) -> None:
    """Select the stem and leaf holders as the generated plant."""
    bpy.ops.object.select_all(action="DESELECT")

    for obj in collection.objects:
        if obj == stem or obj.name.startswith("Leaf_Holder_"):
            obj.select_set(True)

    bpy.context.view_layer.objects.active = stem


def report_generation(leaf: bpy.types.Object, spec: LeafSpec) -> None:
    """Print a summary of the generated plant."""
    objects_per_leaf = 2 + spec.secondary_vein_count * 2

    print("------------------------------------")
    print("PROCEDURAL PLANT GENERATED")
    print("------------------------------------")
    print(f"Leaves: {spec.leaf_count}")
    print(f"Objects per leaf: {objects_per_leaf}")
    print(f"Total leaf assembly objects: {spec.leaf_count * objects_per_leaf}")
    print(f"Stem height: {spec.stem_height}")
    print(f"Leaf length: {spec.length}")
    print(f"Leaf width: {spec.width}")
    print(f"Mesh vertices: {len(leaf.data.vertices)}")
    print(f"Mesh faces: {len(leaf.data.polygons)}")
    print(f"Secondary vein pairs: {spec.secondary_vein_count}")
    print(f"Samples per secondary vein: {spec.secondary_vein_samples}")
    print("------------------------------------")


def generate_leaf(spec: LeafSpec | None = None) -> None:
    """Generate the plant described by ``spec`` in the active Blender scene."""
    if spec is None:
        spec = LeafSpec()

    collection = create_collection(COLLECTION_NAME)

    leaf_material = create_material("Leaf_Green", spec.leaf_color)
    vein_material = create_material("Leaf_Vein_Green", spec.vein_color)
    stem_material = create_material("Stem_Green", spec.stem_color)

    leaf = create_leaf_mesh(collection, leaf_material, spec)
    central_vein = create_central_vein(
        central_vein_points(leaf.data, spec),
        collection,
        vein_material,
        spec,
    )
    stem = generate_stem(collection, stem_material, spec)

    attach_leaves(leaf, central_vein, collection, vein_material, spec)
    select_generated_plant(collection, stem)
    report_generation(leaf, spec)


generate_leaf()
