"""Wasp body geometry V3 — organic shapes with sculpted detail.
Uses bmesh for mesh manipulation, vertex colors for black/yellow banding.
High subdivision for smooth organic surfaces.
"""

import bpy
import bmesh
import math
from mathutils import Vector


def create_organic_sphere(name, location, scale, segments=32, rings=24, subdiv=2):
    """Create a smooth organic sphere with subdivision."""
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1.0, segments=segments, ring_count=rings, location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.shade_smooth()

    mod = obj.modifiers.new(name="Subsurf", type="SUBSURF")
    mod.levels = subdiv
    mod.render_levels = subdiv
    return obj


def sculpt_taper(obj, axis='X', start=0.0, end=1.0, min_scale=0.3):
    """Taper mesh vertices along an axis for organic pointed shapes."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)

    # Get bounds along axis
    axis_idx = {'X': 0, 'Y': 1, 'Z': 2}[axis]
    coords = [v.co[axis_idx] for v in bm.verts]
    vmin, vmax = min(coords), max(coords)
    span = vmax - vmin
    if span == 0:
        bpy.ops.object.mode_set(mode='OBJECT')
        return

    for v in bm.verts:
        t = (v.co[axis_idx] - vmin) / span  # 0 to 1
        if t > start:
            factor = 1.0 - ((t - start) / (end - start)) * (1.0 - min_scale)
            factor = max(factor, min_scale)
            for i in range(3):
                if i != axis_idx:
                    v.co[i] *= factor

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')


def add_vertex_colors_banding(obj, bands=5, color_dark=(0.05, 0.03, 0.02, 1.0), color_light=(0.9, 0.72, 0.08, 1.0)):
    """Add alternating black/yellow bands via vertex colors along X axis."""
    mesh = obj.data
    if not mesh.color_attributes:
        mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')

    color_attr = mesh.color_attributes.active_color

    # Get X bounds
    xs = [v.co.x for v in mesh.vertices]
    xmin, xmax = min(xs), max(xs)
    span = xmax - xmin
    if span == 0:
        return

    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            vert_idx = mesh.loops[loop_idx].vertex_index
            x = mesh.vertices[vert_idx].co.x
            t = (x - xmin) / span
            band = int(t * bands * 2) % 2
            color = color_light if band == 0 else color_dark
            color_attr.data[loop_idx].color = color


# ══════════════════════════════════════════════════════════════════════
# HEAD — wider than tall, slightly triangular
# ══════════════════════════════════════════════════════════════════════
head = create_organic_sphere(
    "Head", location=(0.42, 0, 0.02),
    scale=(0.1, 0.13, 0.08), segments=32, rings=24, subdiv=2
)

# ── COMPOUND EYES — large, bulging, glossy ────────────────────────────
for side, y in [("L", 0.095), ("R", -0.095)]:
    eye = create_organic_sphere(
        f"Eye_{side}", location=(0.44, y, 0.04),
        scale=(0.045, 0.055, 0.065), segments=24, rings=18, subdiv=2
    )


# ══════════════════════════════════════════════════════════════════════
# THORAX — barrel-shaped, the powerhouse
# ══════════════════════════════════════════════════════════════════════
thorax = create_organic_sphere(
    "Thorax", location=(0.12, 0, 0),
    scale=(0.18, 0.13, 0.12), segments=32, rings=24, subdiv=2
)


# ══════════════════════════════════════════════════════════════════════
# PETIOLE — the wasp waist, dramatically thin
# ══════════════════════════════════════════════════════════════════════
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.018, depth=0.1, vertices=16, location=(-0.07, 0, -0.015)
)
petiole = bpy.context.active_object
petiole.name = "Petiole"
petiole.rotation_euler = (0, math.radians(88), 0)
bpy.ops.object.shade_smooth()
mod = petiole.modifiers.new("Subsurf", type="SUBSURF")
mod.levels = 2
mod.render_levels = 2


# ══════════════════════════════════════════════════════════════════════
# ABDOMEN — elongated, tapers to stinger, with black/yellow banding
# ══════════════════════════════════════════════════════════════════════
abdomen = create_organic_sphere(
    "Abdomen", location=(-0.3, 0, -0.01),
    scale=(0.28, 0.1, 0.09), segments=48, rings=32, subdiv=2
)

# Apply scale so taper works on actual geometry
bpy.context.view_layer.objects.active = abdomen
bpy.ops.object.select_all(action='DESELECT')
abdomen.select_set(True)
bpy.ops.object.transform_apply(scale=True)

# Taper the rear of the abdomen toward the stinger
sculpt_taper(abdomen, axis='X', start=0.0, end=0.5, min_scale=0.35)

# Add black/yellow vertex color banding
add_vertex_colors_banding(abdomen, bands=4)


# ══════════════════════════════════════════════════════════════════════
# MANDIBLES — sharp angular cutting tools
# ══════════════════════════════════════════════════════════════════════
for side, y_off, y_rot in [("L", 0.025, -20), ("R", -0.025, 20)]:
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.015, radius2=0.002, depth=0.06, vertices=12,
        location=(0.52, y_off, -0.015)
    )
    m = bpy.context.active_object
    m.name = f"Mandible_{side}"
    m.rotation_euler = (math.radians(-12), math.radians(85), math.radians(y_rot))
    bpy.ops.object.shade_smooth()
    mod = m.modifiers.new("Subsurf", type="SUBSURF")
    mod.levels = 1


print("01_wasp_body.py complete — V3 organic body with tapered abdomen + vertex color banding")
