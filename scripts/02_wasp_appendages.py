"""Wasp appendages: wings, legs, antennae, stinger."""

import bpy
import math


# ── WINGS ─────────────────────────────────────────────────────────────
# 4 wings: 2 forewings (larger), 2 hindwings (smaller)
# Wasps have narrow, elongated wings compared to bees
wing_specs = [
    # (name, location, scale, rotation_degrees)
    ("Wing_Fore_L", (0.18, 0.08, 0.16), (0.85, 0.18, 0.015), (8, 5, 15)),
    ("Wing_Fore_R", (0.18, -0.08, 0.16), (0.85, 0.18, 0.015), (8, -5, -15)),
    ("Wing_Hind_L", (0.06, 0.07, 0.15), (0.55, 0.13, 0.012), (8, 8, 18)),
    ("Wing_Hind_R", (0.06, -0.07, 0.15), (0.55, 0.13, 0.012), (8, -8, -18)),
]

for name, loc, scale, rot_deg in wing_specs:
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=loc)
    wing = bpy.context.active_object
    wing.name = name
    wing.scale = scale
    wing.rotation_euler = (
        math.radians(rot_deg[0]),
        math.radians(rot_deg[1]),
        math.radians(rot_deg[2]),
    )
    # Subdivide for smoother shape
    mod = wing.modifiers.new(name="Subsurf", type="SUBSURF")
    mod.levels = 2
    mod.render_levels = 2
    bpy.ops.object.shade_smooth()


# ── LEGS ──────────────────────────────────────────────────────────────
# 6 legs in 3 pairs, each with femur + tibia segments
# Wasps have longer, dangling legs compared to bees
leg_configs = [
    # (position_name, side, origin, femur_rot_deg, tibia_offset, tibia_rot_deg)
    ("Fore", "L", (0.28, 0.12, -0.08), (25, 0, 35), (0.1, -0.13), ((-15, 0, 20))),
    ("Fore", "R", (0.28, -0.12, -0.08), (25, 0, -35), (-0.1, -0.13), ((-15, 0, -20))),
    ("Mid", "L", (0.15, 0.14, -0.1), (20, 0, 40), (0.12, -0.15), ((-10, 0, 18))),
    ("Mid", "R", (0.15, -0.14, -0.1), (20, 0, -40), (-0.12, -0.15), ((-10, 0, -18))),
    ("Hind", "L", (0.02, 0.13, -0.09), (15, 0, 45), (0.13, -0.18), ((-8, 0, 15))),
    ("Hind", "R", (0.02, -0.13, -0.09), (15, 0, -45), (-0.13, -0.18), ((-8, 0, -15))),
]

for pos, side, origin, fem_rot, tib_off, tib_rot in leg_configs:
    # Femur
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.012, depth=0.2, vertices=8, location=origin
    )
    femur = bpy.context.active_object
    femur.name = f"Leg_{pos}_{side}_Femur"
    femur.rotation_euler = (
        math.radians(fem_rot[0]),
        math.radians(fem_rot[1]),
        math.radians(fem_rot[2]),
    )
    bpy.ops.object.shade_smooth()

    # Tibia
    tibia_loc = (
        origin[0] + tib_off[0],
        origin[1] + (0.08 if side == "L" else -0.08),
        origin[2] + tib_off[1],
    )
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.008, depth=0.22, vertices=8, location=tibia_loc
    )
    tibia = bpy.context.active_object
    tibia.name = f"Leg_{pos}_{side}_Tibia"
    tibia.rotation_euler = (
        math.radians(tib_rot[0]),
        math.radians(tib_rot[1]),
        math.radians(tib_rot[2]),
    )
    bpy.ops.object.shade_smooth()


# ── ANTENNAE ──────────────────────────────────────────────────────────
# Two segmented antennae — wasps have longer, more angular antennae than bees
for side, y_off in [("L", 0.04), ("R", -0.04)]:
    # Scape (base segment — thicker, shorter)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.012, depth=0.1, vertices=8,
        location=(0.62, y_off, 0.15)
    )
    scape = bpy.context.active_object
    scape.name = f"Antenna_{side}_Scape"
    scape.rotation_euler = (
        math.radians(-35),
        0,
        math.radians(12 if side == "L" else -12),
    )
    bpy.ops.object.shade_smooth()

    # Flagellum (long whip — thinner, longer)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.006, depth=0.22, vertices=8,
        location=(0.67, y_off * 1.6, 0.26)
    )
    flag = bpy.context.active_object
    flag.name = f"Antenna_{side}_Flagellum"
    flag.rotation_euler = (
        math.radians(-55),
        0,
        math.radians(18 if side == "L" else -18),
    )
    bpy.ops.object.shade_smooth()


# ── STINGER ───────────────────────────────────────────────────────────
# Sharp, smooth ovipositor — the weapon
bpy.ops.mesh.primitive_cone_add(
    radius1=0.022, radius2=0.001, depth=0.14, vertices=8,
    location=(-0.8, 0, -0.04)
)
stinger = bpy.context.active_object
stinger.name = "Stinger"
stinger.rotation_euler = (0, math.radians(95), 0)
bpy.ops.object.shade_smooth()


print("02_wasp_appendages.py complete — Wings, Legs, Antennae, Stinger created")
