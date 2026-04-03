"""Wasp body geometry: head, thorax, petiole, abdomen, mandibles, eyes."""

import bpy
import math


# ── HEAD ──────────────────────────────────────────────────────────────
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, segments=24, ring_count=16, location=(0.55, 0, 0.05)
)
head = bpy.context.active_object
head.name = "Head"
head.scale = (1.0, 0.85, 0.9)
bpy.ops.object.shade_smooth()

# Compound eyes — large, prominent, dark
for side, y_offset in [("L", 0.09), ("R", -0.09)]:
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.075, segments=16, ring_count=12,
        location=(0.58, y_offset, 0.08)
    )
    eye = bpy.context.active_object
    eye.name = f"Eye_{side}"
    eye.scale = (0.65, 0.85, 1.0)
    bpy.ops.object.shade_smooth()


# ── THORAX ────────────────────────────────────────────────────────────
# Main thorax — powerhouse segment, slightly boxy for wasps
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.22, segments=24, ring_count=16, location=(0.15, 0, 0)
)
thorax = bpy.context.active_object
thorax.name = "Thorax"
thorax.scale = (1.3, 0.85, 0.9)
bpy.ops.object.shade_smooth()

mod = thorax.modifiers.new(name="Subsurf", type="SUBSURF")
mod.levels = 2
mod.render_levels = 2


# ── PETIOLE (wasp waist) ─────────────────────────────────────────────
# The defining feature — thin, elongated connection between thorax and abdomen
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.035, depth=0.18, vertices=12, location=(-0.12, 0, -0.02)
)
petiole = bpy.context.active_object
petiole.name = "Petiole"
petiole.rotation_euler = (0, math.radians(85), 0)
bpy.ops.object.shade_smooth()

# Slight taper — scale one end thinner
mod = petiole.modifiers.new(name="Subsurf", type="SUBSURF")
mod.levels = 1
mod.render_levels = 2


# ── ABDOMEN ───────────────────────────────────────────────────────────
# Elongated, tapering toward the stinger. Wasps have a more pointed abdomen than bees.
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.2, segments=24, ring_count=16, location=(-0.45, 0, -0.03)
)
abdomen = bpy.context.active_object
abdomen.name = "Abdomen"
abdomen.scale = (1.9, 0.7, 0.75)
bpy.ops.object.shade_smooth()

mod = abdomen.modifiers.new(name="Subsurf", type="SUBSURF")
mod.levels = 2
mod.render_levels = 2


# ── MANDIBLES ─────────────────────────────────────────────────────────
# Two sharp, curved cutting tools at front of head
for side, y_rot in [("L", -20), ("R", 20)]:
    y_off = 0.035 if side == "L" else -0.035
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.025, radius2=0.003, depth=0.09, vertices=8,
        location=(0.7, y_off, -0.02)
    )
    mandible = bpy.context.active_object
    mandible.name = f"Mandible_{side}"
    mandible.rotation_euler = (
        math.radians(-10),
        math.radians(90),
        math.radians(y_rot)
    )
    bpy.ops.object.shade_smooth()


print("01_wasp_body.py complete — Head, Eyes, Thorax, Petiole, Abdomen, Mandibles created")
