"""Wasp appendages: wings, legs, antennae, stinger.
V2 — larger wings, better leg articulation, more visible appendages.
"""

import bpy
import math


def smooth_and_subdiv(obj, levels=2):
    bpy.ops.object.shade_smooth()
    mod = obj.modifiers.new(name="Subsurf", type="SUBSURF")
    mod.levels = levels
    mod.render_levels = levels


# ── WINGS ─────────────────────────────────────────────────────────────
# Larger, more visible. Wasps have long narrow wings that extend past the body.
wing_specs = [
    # (name, location, scale, rotation_degrees)
    ("Wing_Fore_L", (0.12, 0.06, 0.14),  (0.45, 0.12, 0.008), (5, 3, 20)),
    ("Wing_Fore_R", (0.12, -0.06, 0.14), (0.45, 0.12, 0.008), (5, -3, -20)),
    ("Wing_Hind_L", (0.04, 0.05, 0.13),  (0.3, 0.09, 0.006),  (5, 5, 24)),
    ("Wing_Hind_R", (0.04, -0.05, 0.13), (0.3, 0.09, 0.006),  (5, -5, -24)),
]

for name, loc, scale, rot_deg in wing_specs:
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=loc)
    wing = bpy.context.active_object
    wing.name = name
    wing.scale = scale
    wing.rotation_euler = tuple(math.radians(r) for r in rot_deg)
    smooth_and_subdiv(wing)


# ── LEGS ──────────────────────────────────────────────────────────────
# 6 legs, 3 pairs. Wasps have notably long, dangling legs.
leg_configs = [
    # (pos, side, femur_loc, femur_rot, tibia_offset, tibia_rot)
    ("Fore", "L",  (0.22, 0.1, -0.06),   (30, 0, 40),   (0.06, 0.06, -0.14),  (-20, 0, 20)),
    ("Fore", "R",  (0.22, -0.1, -0.06),  (30, 0, -40),  (0.06, -0.06, -0.14), (-20, 0, -20)),
    ("Mid",  "L",  (0.12, 0.12, -0.08),  (25, 0, 45),   (0.06, 0.08, -0.16),  (-15, 0, 18)),
    ("Mid",  "R",  (0.12, -0.12, -0.08), (25, 0, -45),  (0.06, -0.08, -0.16), (-15, 0, -18)),
    ("Hind", "L",  (0.02, 0.11, -0.07),  (20, 0, 50),   (0.05, 0.1, -0.18),   (-10, 0, 15)),
    ("Hind", "R",  (0.02, -0.11, -0.07), (20, 0, -50),  (0.05, -0.1, -0.18),  (-10, 0, -15)),
]

for pos, side, fem_loc, fem_rot, tib_off, tib_rot in leg_configs:
    # Femur
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.009, depth=0.16, vertices=8, location=fem_loc
    )
    femur = bpy.context.active_object
    femur.name = f"Leg_{pos}_{side}_Femur"
    femur.rotation_euler = tuple(math.radians(r) for r in fem_rot)
    bpy.ops.object.shade_smooth()

    # Tibia (offset from femur)
    tibia_loc = (
        fem_loc[0] + tib_off[0],
        fem_loc[1] + tib_off[1],
        fem_loc[2] + tib_off[2],
    )
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.006, depth=0.2, vertices=8, location=tibia_loc
    )
    tibia = bpy.context.active_object
    tibia.name = f"Leg_{pos}_{side}_Tibia"
    tibia.rotation_euler = tuple(math.radians(r) for r in tib_rot)
    bpy.ops.object.shade_smooth()


# ── ANTENNAE ──────────────────────────────────────────────────────────
# Wasp antennae: elbowed, segmented, longer than bee antennae
for side, y_off in [("L", 0.035), ("R", -0.035)]:
    sign = 1 if side == "L" else -1

    # Scape (base — thicker, angled)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.009, depth=0.08, vertices=8,
        location=(0.48, y_off, 0.1)
    )
    scape = bpy.context.active_object
    scape.name = f"Antenna_{side}_Scape"
    scape.rotation_euler = (math.radians(-40), 0, math.radians(10 * sign))
    bpy.ops.object.shade_smooth()

    # Flagellum (long whip — thinner)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.005, depth=0.18, vertices=8,
        location=(0.52, y_off * 1.8, 0.18)
    )
    flag = bpy.context.active_object
    flag.name = f"Antenna_{side}_Flagellum"
    flag.rotation_euler = (math.radians(-55), 0, math.radians(15 * sign))
    bpy.ops.object.shade_smooth()


# ── STINGER ───────────────────────────────────────────────────────────
# Sharp, smooth, the weapon. Prominent.
bpy.ops.mesh.primitive_cone_add(
    radius1=0.018, radius2=0.001, depth=0.1, vertices=12,
    location=(-0.6, 0, -0.02)
)
stinger = bpy.context.active_object
stinger.name = "Stinger"
stinger.rotation_euler = (0, math.radians(92), 0)
smooth_and_subdiv(stinger, 1)


print("02_wasp_appendages.py complete — Wings, Legs, Antennae, Stinger")
