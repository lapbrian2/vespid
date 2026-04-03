"""Wasp body geometry: head, thorax, petiole, abdomen, mandibles, eyes.
V2 — improved proportions, more organic feel, better wasp anatomy.
"""

import bpy
import bmesh
import math


def smooth_and_subdiv(obj, levels=2):
    """Apply smooth shading and subdivision surface."""
    bpy.ops.object.shade_smooth()
    mod = obj.modifiers.new(name="Subsurf", type="SUBSURF")
    mod.levels = levels
    mod.render_levels = levels


# ── HEAD ──────────────────────────────────────────────────────────────
# Wasps have a wider, flatter head than bees — almost triangular from above
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.12, segments=32, ring_count=24, location=(0.42, 0, 0.03)
)
head = bpy.context.active_object
head.name = "Head"
head.scale = (0.9, 1.1, 0.75)  # Wide, flat
smooth_and_subdiv(head)

# Compound eyes — large, bulging, wrap around the sides
for side, y_offset in [("L", 0.1), ("R", -0.1)]:
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.065, segments=20, ring_count=16,
        location=(0.44, y_offset, 0.05)
    )
    eye = bpy.context.active_object
    eye.name = f"Eye_{side}"
    eye.scale = (0.7, 0.8, 1.0)
    smooth_and_subdiv(eye, 1)


# ── THORAX ────────────────────────────────────────────────────────────
# The powerhouse — barrel-shaped, slightly wider than tall
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.17, segments=32, ring_count=24, location=(0.12, 0, 0)
)
thorax = bpy.context.active_object
thorax.name = "Thorax"
thorax.scale = (1.2, 0.9, 0.85)
smooth_and_subdiv(thorax)


# ── PETIOLE (wasp waist) ─────────────────────────────────────────────
# THE defining feature. Dramatically thin — makes the wasp a wasp.
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.025, depth=0.12, vertices=16, location=(-0.08, 0, -0.02)
)
petiole = bpy.context.active_object
petiole.name = "Petiole"
petiole.rotation_euler = (0, math.radians(88), 0)
smooth_and_subdiv(petiole, 1)


# ── ABDOMEN ───────────────────────────────────────────────────────────
# Elongated, sleek, pointed toward stinger. Larger than thorax.
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.16, segments=32, ring_count=24, location=(-0.32, 0, -0.01)
)
abdomen = bpy.context.active_object
abdomen.name = "Abdomen"
abdomen.scale = (2.0, 0.65, 0.6)  # Long, narrow, slightly flat
smooth_and_subdiv(abdomen)


# ── MANDIBLES ─────────────────────────────────────────────────────────
# Two sharp, angular cutting tools
for side, y_off, y_rot in [("L", 0.03, -25), ("R", -0.03, 25)]:
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.02, radius2=0.002, depth=0.07, vertices=8,
        location=(0.54, y_off, -0.02)
    )
    mandible = bpy.context.active_object
    mandible.name = f"Mandible_{side}"
    mandible.rotation_euler = (
        math.radians(-15),
        math.radians(85),
        math.radians(y_rot)
    )
    smooth_and_subdiv(mandible, 1)


print("01_wasp_body.py complete — Head, Eyes, Thorax, Petiole, Abdomen, Mandibles")
