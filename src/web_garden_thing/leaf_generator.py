
import bpy
import math
import bmesh
from mathutils import Vector


# ==================================================
# Procedural plant generator
# ==================================================


# --- Leaf parameters ---

LENGTH = 2.0
WIDTH = 0.65

LONGITUDINAL_CURVE = 0.12
CENTRAL_RIDGE = 0.10

BASE_TAPER = 0.8
TIP_SHARPNESS = 1.4

ASYMMETRY = 0.06
CROSS_SECTION_CUP = 0.045

ROWS = 9
COLUMNS = 5


# --- Leaf distribution ---

LEAF_COUNT = 6

LEAF_HEIGHT_MIN = 0.35
LEAF_HEIGHT_MAX = 2.0

GOLDEN_ANGLE = 137.5
LEAF_ANGLE_OFFSET = 0.0
LEAF_ANGLE_VARIATION = 5.0

LEAF_ELEVATION_MIN = -8.0
LEAF_ELEVATION_MAX = 25.0
LEAF_ELEVATION_VARIATION = 4.0

LEAF_SCALE_MIN = 0.75
LEAF_SCALE_MAX = 1.0


# --- Vein parameters ---

CENTRAL_VEIN_THICKNESS = 0.009

SECONDARY_VEIN_COUNT = 6

# Width of a secondary vein at its base.
SECONDARY_VEIN_WIDTH = 0.008

# Offset above the leaf surface to prevent overlap.
SECONDARY_VEIN_OFFSET = 0.002

# Samples along each secondary vein.
SECONDARY_VEIN_SAMPLES = 25

# Start position, spacing, and reach of secondary veins.
SECONDARY_VEIN_START = 0.18
SECONDARY_VEIN_SPACING = 0.12
SECONDARY_VEIN_REACH = 0.08


# --- Stem parameters ---

STEM_HEIGHT = 2.5

STEM_BASE_RADIUS = 0.045
STEM_TIP_RADIUS = 0.018

STEM_BEND_X = 0.15
STEM_BEND_Y = 0.05

STEM_SEGMENTS = 12
STEM_SIDES = 6

STEM_COLOUR = (0.10, 0.25, 0.07, 1.0)


# --- Material parameters ---

COLOUR = (0.12, 0.32, 0.09, 1.0)
VEIN_COLOUR = (0.22, 0.42, 0.14, 1.0)


# --- Collection setup ---

COLLECTION_NAME = "Plant Generator"

collection = bpy.data.collections.get(COLLECTION_NAME)

if collection is None:
    collection = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(collection)

for obj in list(collection.objects):
    bpy.data.objects.remove(obj, do_unlink=True)


# --- Material creation ---

def create_material(name, colour):

    material = bpy.data.materials.get(name)

    if material is None:
        material = bpy.data.materials.new(name)

    material.diffuse_color = colour
    material.use_nodes = True

    principled = material.node_tree.nodes.get("Principled BSDF")

    if principled:
        principled.inputs["Base Color"].default_value = colour
        principled.inputs["Roughness"].default_value = 0.85

    return material


leaf_material = create_material("Leaf_Green", COLOUR)
vein_material = create_material("Leaf_Vein_Green", VEIN_COLOUR)
stem_material = create_material("Stem_Green", STEM_COLOUR)


# --- Leaf surface ---

def leaf_surface(u, t):

    if t <= 0.0 or t >= 1.0:
        return (0.0, LENGTH * t, 0.0)

    width_profile = (
        math.sin(math.pi * t) ** (1.0 / TIP_SHARPNESS)
    )

    width_profile *= (
        BASE_TAPER + (1.0 - BASE_TAPER) * t
    )

    x = u * WIDTH * 0.5 * width_profile

    x += (
        ASYMMETRY
        * WIDTH
        * math.sin(math.pi * t)
    )

    y = LENGTH * t

    ridge = CENTRAL_RIDGE * (1.0 - abs(u))
    cup = CROSS_SECTION_CUP * (abs(u) ** 1.7)
    bend = LONGITUDINAL_CURVE * math.sin(math.pi * t)

    z = ridge - cup + bend

    return (x, y, z)


# --- Generate leaf mesh ---

vertices = []
faces = []

vertices.append((0.0, 0.0, 0.0))

for row in range(1, ROWS + 1):

    t = row / (ROWS + 1)

    for col in range(COLUMNS):

        u = (
            (col / (COLUMNS - 1)) * 2.0 - 1.0
        )

        vertices.append(leaf_surface(u, t))


tip_index = len(vertices)

vertices.append((0.0, LENGTH, 0.0))


# Close the leaf base with triangles.
for col in range(COLUMNS - 1):

    faces.append((
        0,
        col + 2,
        col + 1
    ))


# Fill the leaf interior with triangles.
for row in range(ROWS - 1):

    current = 1 + row * COLUMNS
    next_row = current + COLUMNS

    for col in range(COLUMNS - 1):

        a = current + col
        b = current + col + 1
        c = next_row + col + 1
        d = next_row + col

        faces.append((a, b, c))
        faces.append((a, c, d))


# Close the leaf tip with triangles.
last_row = 1 + (ROWS - 1) * COLUMNS

for col in range(COLUMNS - 1):

    faces.append((
        last_row + col,
        last_row + col + 1,
        tip_index
    ))


mesh = bpy.data.meshes.new("Leaf_Mesh")
mesh.from_pydata(vertices, [], faces)
mesh.update()

leaf = bpy.data.objects.new("Leaf_Prototype", mesh)
collection.objects.link(leaf)

leaf.data.materials.append(leaf_material)

for polygon in mesh.polygons:
    polygon.use_smooth = False


# --- Leaf properties ---

leaf["length"] = LENGTH
leaf["width"] = WIDTH
leaf["longitudinal_curve"] = LONGITUDINAL_CURVE
leaf["central_ridge"] = CENTRAL_RIDGE
leaf["base_taper"] = BASE_TAPER
leaf["tip_sharpness"] = TIP_SHARPNESS
leaf["asymmetry"] = ASYMMETRY
leaf["cross_section_cup"] = CROSS_SECTION_CUP
leaf["rows"] = ROWS
leaf["columns"] = COLUMNS


# --- Sample leaf surface ---

def sample_leaf_surface(target_mesh, u, t):
    """
    Interpolate a point and normal on the triangulated leaf mesh.
    """

    t = max(
        1.0 / (ROWS + 1),
        min(t, ROWS / (ROWS + 1))
    )

    u = max(-1.0, min(u, 1.0))

    column_position = (
        (u + 1.0) * 0.5 * (COLUMNS - 1)
    )

    column = min(
        int(math.floor(column_position)),
        COLUMNS - 2
    )

    x = column_position - column

    row_position = t * (ROWS + 1)

    row = int(math.floor(row_position))
    row = max(1, min(row, ROWS - 1))

    y = row_position - row

    a_index = 1 + (row - 1) * COLUMNS + column
    b_index = a_index + 1
    d_index = a_index + COLUMNS
    c_index = d_index + 1

    a = Vector(target_mesh.vertices[a_index].co)
    b = Vector(target_mesh.vertices[b_index].co)
    c = Vector(target_mesh.vertices[c_index].co)
    d = Vector(target_mesh.vertices[d_index].co)

    if y <= x:

        point = (
            a * (1.0 - x)
            + b * (x - y)
            + c * y
        )

        normal = (b - a).cross(c - a)

    else:

        point = (
            a * (1.0 - y)
            + c * x
            + d * (y - x)
        )

        normal = (c - a).cross(d - a)

    normal.normalize()

    return point, normal


# --- Create central vein ---

def create_central_vein(points):

    curve_data = bpy.data.curves.new(
        "Central_Vein_Curve",
        "CURVE"
    )

    curve_data.dimensions = "3D"
    curve_data.resolution_u = 1

    curve_data.bevel_depth = CENTRAL_VEIN_THICKNESS
    curve_data.bevel_resolution = 0

    spline = curve_data.splines.new("POLY")
    spline.points.add(len(points) - 1)

    for i, point in enumerate(points):

        spline.points[i].co = (
            point.x,
            point.y,
            point.z,
            1.0
        )

    vein = bpy.data.objects.new(
        "Leaf_Central_Vein",
        curve_data
    )

    collection.objects.link(vein)
    vein.data.materials.append(vein_material)

    vein["vein_type"] = "central"

    return vein


central_points = [
    mesh.vertices[0].co.copy()
]

middle_column = COLUMNS // 2

for row in range(ROWS):

    vertex_index = 1 + row * COLUMNS + middle_column

    central_points.append(
        mesh.vertices[vertex_index].co.copy()
    )

central_points.append(
    mesh.vertices[-1].co.copy()
)

central_vein = create_central_vein(central_points)


# --- Deform leaf mesh ---

def deform_leaf_mesh(obj, sweep, droop):

    for vertex in obj.data.vertices:

        co = vertex.co

        t = max(
            0.0,
            min(co.y / LENGTH, 1.0)
        )

        profile = math.sin(math.pi * t)

        co.x += sweep * profile
        co.z += droop * profile

    obj.data.update()


# --- Create secondary vein mesh ---

def create_secondary_vein_mesh(
    leaf_mesh,
    vein_index,
    side
):
    """
    Build a tapered ribbon that follows the triangulated leaf surface.

    Sample each ribbon vertex directly from the leaf mesh.
    """

    ribbon_vertices = []
    ribbon_faces = []

    start_t = (
        SECONDARY_VEIN_START
        + vein_index * SECONDARY_VEIN_SPACING
    )

    for step in range(SECONDARY_VEIN_SAMPLES + 1):

        progress = step / SECONDARY_VEIN_SAMPLES

        u = side * 0.85 * progress

        t = (
            start_t
            + SECONDARY_VEIN_REACH * progress
        )

        point, normal = sample_leaf_surface(
            leaf_mesh.data,
            u,
            t
        )

        # Estimate the vein tangent from nearby surface samples.
        previous_progress = max(0.0, progress - 0.001)
        next_progress = min(1.0, progress + 0.001)

        previous_point, _ = sample_leaf_surface(
            leaf_mesh.data,
            side * 0.85 * previous_progress,
            start_t + SECONDARY_VEIN_REACH * previous_progress
        )

        next_point, _ = sample_leaf_surface(
            leaf_mesh.data,
            side * 0.85 * next_progress,
            start_t + SECONDARY_VEIN_REACH * next_progress
        )

        tangent = (next_point - previous_point).normalized()

        # Find the direction across the vein.
        lateral = tangent.cross(normal).normalized()

        # Taper the ribbon toward the outer end.
        width_profile = (
            0.12 + 0.88 * (1.0 - progress) ** 0.8
        )

        half_width = (
            SECONDARY_VEIN_WIDTH
            * width_profile
            * 0.5
        )

        # Lift the ribbon slightly to prevent z-fighting.
        surface_point = (
            point
            + normal * SECONDARY_VEIN_OFFSET
        )

        left = (
            surface_point
            - lateral * half_width
        )

        right = (
            surface_point
            + lateral * half_width
        )

        ribbon_vertices.append(tuple(left))
        ribbon_vertices.append(tuple(right))


    # Join consecutive left-right pairs into a continuous strip.
    for step in range(SECONDARY_VEIN_SAMPLES):

        a = step * 2
        b = a + 1
        c = a + 3
        d = a + 2

        ribbon_faces.append((a, b, c, d))


    # Build the mesh from the ribbon geometry.
    vein_mesh = bpy.data.meshes.new(
        f"Secondary_Vein_Mesh_{vein_index}_{side}"
    )

    vein_mesh.from_pydata(
        ribbon_vertices,
        [],
        ribbon_faces
    )

    vein_mesh.update()

    vein = bpy.data.objects.new(
        f"Leaf_Secondary_Vein_{vein_index}_{side}",
        vein_mesh
    )

    collection.objects.link(vein)
    vein.data.materials.append(vein_material)

    vein["vein_type"] = "secondary"
    vein["vein_index"] = vein_index
    vein["vein_side"] = side

    for polygon in vein_mesh.polygons:
        polygon.use_smooth = False

    return vein


# --- Regenerate central vein ---

def regenerate_central_vein(leaf_mesh, vein):

    points = [
        leaf_mesh.data.vertices[0].co.copy()
    ]

    middle_column = COLUMNS // 2

    for row in range(ROWS):

        vertex_index = 1 + row * COLUMNS + middle_column

        points.append(
            leaf_mesh.data.vertices[vertex_index].co.copy()
        )

    points.append(
        leaf_mesh.data.vertices[-1].co.copy()
    )

    spline = vein.data.splines[0]

    for i, point in enumerate(points):

        spline.points[i].co = (
            point.x,
            point.y,
            point.z,
            1.0
        )


# --- Generate stem ---

def generate_stem():

    vertices = []
    faces = []

    for segment in range(STEM_SEGMENTS + 1):

        t = segment / STEM_SEGMENTS

        center = Vector((
            STEM_BEND_X * t ** 2,
            STEM_BEND_Y * math.sin(math.pi * t),
            STEM_HEIGHT * t
        ))

        tangent = Vector((
            2.0 * STEM_BEND_X * t,
            STEM_BEND_Y * math.pi * math.cos(math.pi * t),
            STEM_HEIGHT
        )).normalized()

        reference = Vector((0.0, 1.0, 0.0))

        axis_u = tangent.cross(reference).normalized()
        axis_v = tangent.cross(axis_u).normalized()

        radius = (
            STEM_BASE_RADIUS * (1.0 - t)
            + STEM_TIP_RADIUS * t
        )

        for side in range(STEM_SIDES):

            angle = (side / STEM_SIDES) * math.tau

            offset = (
                axis_u * math.cos(angle)
                + axis_v * math.sin(angle)
            ) * radius

            vertices.append(tuple(center + offset))


    for segment in range(STEM_SEGMENTS):

        for side in range(STEM_SIDES):

            current = segment * STEM_SIDES + side
            next_side = (side + 1) % STEM_SIDES

            a = current
            b = segment * STEM_SIDES + next_side

            c = (segment + 1) * STEM_SIDES + next_side
            d = (segment + 1) * STEM_SIDES + side

            faces.append((a, b, c, d))


    faces.append(tuple(
        range(STEM_SIDES - 1, -1, -1)
    ))

    tip_start = STEM_SEGMENTS * STEM_SIDES

    faces.append(tuple(
        tip_start + side
        for side in range(STEM_SIDES)
    ))


    stem_mesh = bpy.data.meshes.new("Stem_Mesh")

    stem_mesh.from_pydata(vertices, [], faces)
    stem_mesh.update()

    bm = bmesh.new()
    bm.from_mesh(stem_mesh)

    bmesh.ops.recalc_face_normals(
        bm,
        faces=bm.faces
    )

    bm.to_mesh(stem_mesh)
    bm.free()

    stem_mesh.update()

    stem = bpy.data.objects.new(
        "Stem_Prototype",
        stem_mesh
    )

    collection.objects.link(stem)
    stem.data.materials.append(stem_material)

    for polygon in stem_mesh.polygons:
        polygon.use_smooth = False

    stem["height"] = STEM_HEIGHT
    stem["base_radius"] = STEM_BASE_RADIUS
    stem["tip_radius"] = STEM_TIP_RADIUS
    stem["bend_x"] = STEM_BEND_X
    stem["bend_y"] = STEM_BEND_Y
    stem["segments"] = STEM_SEGMENTS
    stem["sides"] = STEM_SIDES

    return stem


stem = generate_stem()


# --- Attach and distribute leaves ---

def attach_leaves():

    leaf_parts = [
        leaf,
        central_vein
    ]

    for i in range(LEAF_COUNT):

        progress = i / max(LEAF_COUNT - 1, 1)

        # Set the leaf's orientation.

        angle = (
            math.radians(i * GOLDEN_ANGLE)
            + math.radians(LEAF_ANGLE_OFFSET)
            + math.radians(
                math.sin(i * 2.1) * LEAF_ANGLE_VARIATION
            )
        )

        elevation_degrees = (
            LEAF_ELEVATION_MIN
            + (LEAF_ELEVATION_MAX - LEAF_ELEVATION_MIN)
            * progress
        )

        elevation_degrees += (
            math.sin(i * 1.7) * LEAF_ELEVATION_VARIATION
        )

        elevation = math.radians(elevation_degrees)

        direction = Vector((
            math.cos(angle) * math.cos(elevation),
            math.sin(angle) * math.cos(elevation),
            math.sin(elevation)
        )).normalized()


        # Place the leaf along the stem.

        height = (
            LEAF_HEIGHT_MIN
            + (LEAF_HEIGHT_MAX - LEAF_HEIGHT_MIN) * progress
        )


        # Create a holder for the leaf assembly.

        holder = bpy.data.objects.new(
            f"Leaf_Holder_{i + 1}",
            None
        )

        collection.objects.link(holder)

        holder.location = Vector((
            STEM_BEND_X * (height / STEM_HEIGHT) ** 2,
            STEM_BEND_Y * math.sin(
                math.pi * height / STEM_HEIGHT
            ),
            height
        ))

        holder.rotation_mode = "QUATERNION"

        holder.rotation_quaternion = direction.to_track_quat(
            "Y",
            "Z"
        )


        # Scale the leaf based on its position along the stem.

        variation = (
            0.94 + 0.06 * math.sin(i * 2.4)
        )

        scale = (
            LEAF_SCALE_MIN
            + (LEAF_SCALE_MAX - LEAF_SCALE_MIN) * progress
        ) * variation

        holder.scale = (scale, scale, scale)


        # Duplicate the leaf and central vein prototypes.

        duplicates = {}

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


        leaf_mesh = duplicates["Leaf_Prototype"]
        central = duplicates["Leaf_Central_Vein"]


        # Deform this leaf independently.

        sweep = math.sin(i * 2.3) * 0.08
        droop = math.sin(i * 1.7) * 0.12

        deform_leaf_mesh(
            leaf_mesh,
            sweep,
            droop
        )


        # Match the central vein to the deformed leaf.

        regenerate_central_vein(
            leaf_mesh,
            central
        )


        # Add secondary vein meshes to the leaf.

        for vein_index in range(SECONDARY_VEIN_COUNT):

            for side in [-1, 1]:

                vein = create_secondary_vein_mesh(
                    leaf_mesh,
                    vein_index,
                    side
                )

                vein.parent = holder
                vein.matrix_parent_inverse.identity()

                vein.location = (0.0, 0.0, 0.0)
                vein.rotation_euler = (0.0, 0.0, 0.0)
                vein.scale = (1.0, 1.0, 1.0)


    # Hide the original prototypes.

    for original in leaf_parts:

        original.hide_set(True)
        original.hide_render = True


attach_leaves()


# --- Select generated plant ---

bpy.ops.object.select_all(action="DESELECT")

for obj in collection.objects:

    if (
        obj == stem
        or obj.name.startswith("Leaf_Holder_")
    ):
        obj.select_set(True)

bpy.context.view_layer.objects.active = stem


# --- Completion report ---

objects_per_leaf = (
    2 + SECONDARY_VEIN_COUNT * 2
)

print("------------------------------------")
print("PROCEDURAL PLANT GENERATED")
print("------------------------------------")
print(f"Leaves: {LEAF_COUNT}")
print(f"Objects per leaf: {objects_per_leaf}")
print(f"Total leaf assembly objects: {LEAF_COUNT * objects_per_leaf}")
print(f"Stem height: {STEM_HEIGHT}")
print(f"Leaf length: {LENGTH}")
print(f"Leaf width: {WIDTH}")
print(f"Mesh vertices: {len(mesh.vertices)}")
print(f"Mesh faces: {len(mesh.polygons)}")
print(f"Secondary vein pairs: {SECONDARY_VEIN_COUNT}")
print(f"Samples per secondary vein: {SECONDARY_VEIN_SAMPLES}")
print("------------------------------------")
