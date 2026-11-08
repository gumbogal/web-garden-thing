
import bpy
import math
import bmesh
from mathutils import Vector

# ==================================================
# PROCEDURAL LEAF GENERATOR
# ==================================================

# --------------------------------------------------
# 1. LEAF PARAMETERS
# --------------------------------------------------

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

# LEAF DISTRIBUTION
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


# --------------------------------------------------
# 2. VEIN PARAMETERS
# --------------------------------------------------

CENTRAL_VEIN_THICKNESS = 0.009
SECONDARY_VEIN_THICKNESS = 0.0035

SECONDARY_VEIN_COUNT = 6

# --------------------------------------------------
# 3. STEM PARAMETERS
# --------------------------------------------------

STEM_HEIGHT = 2.5

STEM_BASE_RADIUS = 0.045
STEM_TIP_RADIUS = 0.018

STEM_BEND_X = 0.15
STEM_BEND_Y = 0.05

STEM_SEGMENTS = 12
STEM_SIDES = 6

STEM_COLOUR = (0.10, 0.25, 0.07, 1.0)


# --------------------------------------------------
# 4. MATERIAL PARAMETERS
# --------------------------------------------------

COLOUR = (0.12, 0.32, 0.09, 1.0)
VEIN_COLOUR = (0.22, 0.42, 0.14, 1.0)


# --------------------------------------------------
# 5. COLLECTION SETUP
# --------------------------------------------------

COLLECTION_NAME = "Plant Generator"

collection = bpy.data.collections.get(COLLECTION_NAME)

if collection is None:
    collection = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(collection)

# Remove previous generated objects
for obj in list(collection.objects):
    bpy.data.objects.remove(obj, do_unlink=True)


# --------------------------------------------------
# 6. SHARED LEAF SURFACE FUNCTION
# --------------------------------------------------

def leaf_surface(u, t):

    # Ensure the base and tip terminate at a single point
    if t <= 0.0 or t >= 1.0:
        return (0.0, LENGTH * t, 0.0)

    # Leaf width profile
    width_profile = (
        math.sin(math.pi * t) ** (1.0 / TIP_SHARPNESS)
    )

    # Gradually widen towards the upper portion
    width_profile *= (
        BASE_TAPER + (1.0 - BASE_TAPER) * t
    )

    # Horizontal position
    x = u * WIDTH * 0.5 * width_profile

    # Subtle natural asymmetry
    x += ASYMMETRY * WIDTH * math.sin(math.pi * t)

    # Longitudinal position
    y = LENGTH * t

    # Raised central ridge
    ridge = CENTRAL_RIDGE * (1.0 - abs(u))

    # Concave cross-section
    cup = CROSS_SECTION_CUP * (abs(u) ** 1.7)

    # Longitudinal curvature
    bend = LONGITUDINAL_CURVE * math.sin(math.pi * t)

    z = ridge - cup + bend

    return (x, y, z)


# --------------------------------------------------
# 7. GEOMETRY GENERATION
# --------------------------------------------------

vertices = []
faces = []

# Base attachment point
vertices.append((0.0, 0.0, 0.0))

base_index = 0

# Generate leaf surface vertices
for row in range(1, ROWS + 1):

    t = row / (ROWS + 1)

    for col in range(COLUMNS):

        u = (col / (COLUMNS - 1)) * 2.0 - 1.0

        vertices.append(leaf_surface(u, t))


# Tip vertex
tip_index = len(vertices)

vertices.append((0.0, LENGTH, 0.0))


# --------------------------------------------------
# 8. BUILD TRIANGULAR FACES
# --------------------------------------------------

first_row = 1

# Connect base to first row
for col in range(COLUMNS - 1):

    faces.append((
        base_index,
        first_row + col + 1,
        first_row + col
    ))


# Connect interior rows
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


# Connect final row to tip
last_row = 1 + (ROWS - 1) * COLUMNS

for col in range(COLUMNS - 1):

    faces.append((
        last_row + col,
        last_row + col + 1,
        tip_index
    ))


# --------------------------------------------------
# 9. CREATE BLENDER MESH
# --------------------------------------------------

mesh = bpy.data.meshes.new("Leaf_Mesh")

mesh.from_pydata(vertices, [], faces)
mesh.update()



def sample_leaf_mesh(u, t):
    """
    Interpolate across the actual triangles of the leaf mesh.

    This version uses the same longitudinal spacing as
    the mesh generator and samples its actual vertices.
    """

    # Keep sampling within the interior triangulated grid.
    # The current secondary veins do not reach the end caps.
    t = max(1.0 / (ROWS + 1), min(
        t, ROWS / (ROWS + 1)
    ))

    u = max(-1.0, min(u, 1.0))

    # Horizontal grid position
    column_position = (
        (u + 1.0) * 0.5 * (COLUMNS - 1)
    )

    column = min(
        int(math.floor(column_position)),
        COLUMNS - 2
    )

    x = column_position - column

    # Correct longitudinal grid position
    row_position = t * (ROWS + 1)

    row = int(math.floor(row_position))
    row = max(1, min(row, ROWS - 1))

    y = row_position - row

    # Retrieve actual mesh vertices
    a_index = 1 + (row - 1) * COLUMNS + column
    b_index = a_index + 1
    d_index = a_index + COLUMNS
    c_index = d_index + 1

    a = Vector(mesh.vertices[a_index].co)
    b = Vector(mesh.vertices[b_index].co)
    c = Vector(mesh.vertices[c_index].co)
    d = Vector(mesh.vertices[d_index].co)

    # Interpolate over the actual A-C diagonal.
    if y <= x:
        point = (
            a * (1.0 - x)
            + b * (x - y)
            + c * y
        )
    else:
        point = (
            a * (1.0 - y)
            + c * x
            + d * (y - x)
        )

    return point



leaf = bpy.data.objects.new("Leaf_Prototype", mesh)

collection.objects.link(leaf)

# Flat shading
for polygon in mesh.polygons:
    polygon.use_smooth = False


# --------------------------------------------------
# 10. LEAF MATERIAL
# --------------------------------------------------

material = bpy.data.materials.get("Leaf_Green")

if material is None:
    material = bpy.data.materials.new("Leaf_Green")

material.diffuse_color = COLOUR
material.use_nodes = True

principled = material.node_tree.nodes.get("Principled BSDF")

if principled:
    principled.inputs["Base Color"].default_value = COLOUR
    principled.inputs["Roughness"].default_value = 0.85

leaf.data.materials.clear()
leaf.data.materials.append(material)


# --------------------------------------------------
# 11. STORE GENERATOR PARAMETERS
# --------------------------------------------------

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


# --------------------------------------------------
# 12. VEIN MATERIAL
# --------------------------------------------------

vein_material = bpy.data.materials.get("Leaf_Vein_Green")

if vein_material is None:
    vein_material = bpy.data.materials.new("Leaf_Vein_Green")

vein_material.diffuse_color = VEIN_COLOUR
vein_material.use_nodes = True

principled = vein_material.node_tree.nodes.get("Principled BSDF")

if principled:
    principled.inputs["Base Color"].default_value = VEIN_COLOUR
    principled.inputs["Roughness"].default_value = 0.85


# --------------------------------------------------
# 13. VEIN GENERATION FUNCTION
# --------------------------------------------------

def create_vein(name, points, thickness):

    curve_data = bpy.data.curves.new(name, "CURVE")

    curve_data.dimensions = "3D"
    curve_data.resolution_u = 1

    curve_data.bevel_depth = thickness
    curve_data.bevel_resolution = 0

    spline = curve_data.splines.new("POLY")
    spline.points.add(len(points) - 1)

    for i, position in enumerate(points):

        spline.points[i].co = (
            position[0],
            position[1],
            position[2],
            1.0
        )

    vein = bpy.data.objects.new(name, curve_data)

    collection.objects.link(vein)

    vein.data.materials.append(vein_material)

    return vein


# --------------------------------------------------
# 14. CENTRAL MIDRIB FROM MESH VERTICES
# --------------------------------------------------

central_points = []

# Leaf base
central_points.append(
    mesh.vertices[0].co.copy()
)

# Centre vertex from every row
middle_column = COLUMNS // 2

for row in range(ROWS):

    vertex_index = 1 + row * COLUMNS + middle_column

    central_points.append(
        mesh.vertices[vertex_index].co.copy()
    )

# Leaf tip
central_points.append(
    mesh.vertices[-1].co.copy()
)

create_vein(
    "Leaf_Central_Vein",
    central_points,
    CENTRAL_VEIN_THICKNESS
)


# --------------------------------------------------
# 15. SECONDARY VEINS
# --------------------------------------------------

for i in range(SECONDARY_VEIN_COUNT):

    t = 0.22 + i * 0.12

    for side in [-1, 1]:

        points = []

        for step in range(7):

            progress = step / 6

            u = side * 0.85 * progress
            vein_t = t + 0.09 * progress

            point = sample_leaf_mesh(u, vein_t)
            points.append(point)

        create_vein(
            f"Leaf_Secondary_Vein_{i}_{side}",
            points,
            SECONDARY_VEIN_THICKNESS
        )


# --------------------------------------------------
# 16. STEM GENERATION
# --------------------------------------------------

def generate_stem():

    vertices = []
    faces = []

    # Generate cross-sectional rings
    for segment in range(STEM_SEGMENTS + 1):

        t = segment / STEM_SEGMENTS

        # ------------------------------------------
        # STEM CENTRELINE
        # ------------------------------------------

        center = Vector((
            STEM_BEND_X * t ** 2,
            STEM_BEND_Y * math.sin(math.pi * t),
            STEM_HEIGHT * t
        ))

        # Tangent along the stem
        tangent = Vector((
            2.0 * STEM_BEND_X * t,
            STEM_BEND_Y * math.pi * math.cos(math.pi * t),
            STEM_HEIGHT
        )).normalized()

        # ------------------------------------------
        # CROSS-SECTION ORIENTATION
        # ------------------------------------------

        reference = Vector((0.0, 1.0, 0.0))

        axis_u = tangent.cross(reference).normalized()
        axis_v = tangent.cross(axis_u).normalized()

        # ------------------------------------------
        # TAPER
        # ------------------------------------------

        radius = (
            STEM_BASE_RADIUS * (1.0 - t)
            + STEM_TIP_RADIUS * t
        )

        # ------------------------------------------
        # GENERATE RING VERTICES
        # ------------------------------------------

        for side in range(STEM_SIDES):

            angle = (side / STEM_SIDES) * math.tau

            offset = (
                axis_u * math.cos(angle)
                + axis_v * math.sin(angle)
            ) * radius

            position = center + offset

            vertices.append(tuple(position))

    # ----------------------------------------------
    # CONNECT RINGS WITH QUAD FACES
    # ----------------------------------------------

    for segment in range(STEM_SEGMENTS):

        for side in range(STEM_SIDES):

            current = segment * STEM_SIDES + side
            next_side = (side + 1) % STEM_SIDES

            a = current
            b = segment * STEM_SIDES + next_side

            c = (segment + 1) * STEM_SIDES + next_side
            d = (segment + 1) * STEM_SIDES + side

            faces.append((a, b, c, d))

    # ----------------------------------------------
    # CLOSE STEM ENDS
    # ----------------------------------------------

    faces.append(tuple(
        range(STEM_SIDES - 1, -1, -1)
    ))

    tip_start = STEM_SEGMENTS * STEM_SIDES

    faces.append(tuple(
        tip_start + side
        for side in range(STEM_SIDES)
    ))

    # ----------------------------------------------
    # CREATE MESH
    # ----------------------------------------------

    stem_mesh = bpy.data.meshes.new("Stem_Mesh")

    stem_mesh.from_pydata(vertices, [], faces)
    stem_mesh.update()

    # Recalculate normals
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

    # Flat shading
    for polygon in stem_mesh.polygons:
        polygon.use_smooth = False

    # ----------------------------------------------
    # STEM MATERIAL
    # ----------------------------------------------

    material = bpy.data.materials.get("Stem_Green")

    if material is None:
        material = bpy.data.materials.new("Stem_Green")

    material.diffuse_color = STEM_COLOUR
    material.use_nodes = True

    principled = material.node_tree.nodes.get(
        "Principled BSDF"
    )

    if principled:
        principled.inputs["Base Color"].default_value = STEM_COLOUR
        principled.inputs["Roughness"].default_value = 0.85

    stem.data.materials.append(material)

    # ----------------------------------------------
    # STORE PARAMETERS
    # ----------------------------------------------

    stem["height"] = STEM_HEIGHT
    stem["base_radius"] = STEM_BASE_RADIUS
    stem["tip_radius"] = STEM_TIP_RADIUS

    stem["bend_x"] = STEM_BEND_X
    stem["bend_y"] = STEM_BEND_Y

    stem["segments"] = STEM_SEGMENTS
    stem["sides"] = STEM_SIDES

    return stem


stem = generate_stem()


# --------------------------------------------------
# 16. LEAF ATTACHMENT AND DISTRIBUTION
# --------------------------------------------------

def attach_leaves():
    # Collect the complete leaf prototype:
    # one leaf mesh and all its separate vein objects.
    leaf_parts = [
        obj for obj in collection.objects
        if (
            obj.name == "Leaf_Prototype"
            or obj.name.startswith("Leaf_Central_Vein")
            or obj.name.startswith("Leaf_Secondary_Vein")
        )
    ]

    if not leaf_parts:
        print("No leaf prototype objects found.")
        return

    for i in range(LEAF_COUNT):

        # --------------------------------------------------
        # NATURAL LEAF ORIENTATION
        # --------------------------------------------------

        progress = i / max(LEAF_COUNT - 1, 1)

        # Golden-angle phyllotaxis with subtle variation.
        angle = (
            math.radians(i * GOLDEN_ANGLE)
            + math.radians(LEAF_ANGLE_OFFSET)
            + math.radians(
                math.sin(i * 2.1) * LEAF_ANGLE_VARIATION
            )
        )

        # Gradually increase elevation towards the top.
        elevation_degrees = (
            LEAF_ELEVATION_MIN
            + (LEAF_ELEVATION_MAX - LEAF_ELEVATION_MIN)
            * progress
        )

        # Add individual variation.
        elevation_degrees += (
            math.sin(i * 1.7) * LEAF_ELEVATION_VARIATION
        )

        elevation = math.radians(elevation_degrees)

        # Calculate the direction in which the leaf grows.
        direction = Vector((
            math.cos(angle) * math.cos(elevation),
            math.sin(angle) * math.cos(elevation),
            math.sin(elevation)
        )).normalized()

        # Alternate leaf heights along the stem.
        height = (
            LEAF_HEIGHT_MIN
            + (LEAF_HEIGHT_MAX - LEAF_HEIGHT_MIN) * progress
        )

        # Create a parent Empty at the attachment point.
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

        holder.rotation_mode = 'QUATERNION'
        holder.rotation_quaternion = direction.to_track_quat(
            'Y',
            'Z'
        )

        variation = (
            0.94
            + 0.06 * math.sin(i * 2.4)
        )

        scale = (
            LEAF_SCALE_MIN
            + (LEAF_SCALE_MAX - LEAF_SCALE_MIN) * progress
        ) * variation

        holder.scale = (scale, scale, scale)

        # Duplicate every part of the leaf assembly.
        for original in leaf_parts:

            duplicate = original.copy()

            # Mesh and curve data can be shared.
            duplicate.data = original.data

            collection.objects.link(duplicate)

            # Parent the duplicate to the holder.
            duplicate.parent = holder
            duplicate.matrix_parent_inverse.identity()

            duplicate.location = (0.0, 0.0, 0.0)
            duplicate.rotation_euler = (0.0, 0.0, 0.0)
            duplicate.scale = (1.0, 1.0, 1.0)

    # Hide the original prototype objects.
    # The duplicated leaf assemblies remain visible.
    for original in leaf_parts:
        original.hide_set(True)
        original.hide_render = True


attach_leaves()



# --------------------------------------------------
# 17. SELECT PLANT
# --------------------------------------------------

bpy.ops.object.select_all(action="DESELECT")

for obj in collection.objects:
    if obj == stem or obj.name.startswith("Leaf_Holder_"):
        obj.select_set(True)

bpy.context.view_layer.objects.active = stem


# --------------------------------------------------
# 18. COMPLETION
# --------------------------------------------------

print("------------------------------------")
print("PROCEDURAL LEAF GENERATED")
print("------------------------------------")
print(f"Length: {LENGTH}")
print(f"Width: {WIDTH}")
print(f"Mesh vertices: {len(mesh.vertices)}")
print(f"Mesh faces: {len(mesh.polygons)}")
print(f"Secondary vein pairs: {SECONDARY_VEIN_COUNT}")
print("------------------------------------")
