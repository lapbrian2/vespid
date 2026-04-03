"""Wasp appendages V3 — detailed wings with vein lines, jointed legs,
elbowed antennae, prominent stinger. More organic, less geometric.
"""

import bpy
import bmesh
import math
from mathutils import Vector


def smooth_subdiv(obj, levels=2):
    bpy.ops.object.shade_smooth()
    mod = obj.modifiers.new("Subsurf", type="SUBSURF")
    mod.levels = levels
    mod.render_levels = levels


# ══════════════════════════════════════════════════════════════════════
# WINGS — elongated with subtle curvature and vein lines
# ══════════════════════════════════════════════════════════════════════

def create_wing(name, origin, length, width, angle_z, angle_x=5):
    """Create a wing with curved profile and vein detail."""
    # Main wing membrane — subdivided plane with curvature
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=origin)
    wing = bpy.context.active_object
    wing.name = name
    wing.scale = (length, width, 0.003)
    wing.rotation_euler = (
        math.radians(angle_x),
        math.radians(2),
        math.radians(angle_z),
    )

    # Add curvature via simple deform
    mod_curve = wing.modifiers.new("Bend", type="SIMPLE_DEFORM")
    mod_curve.deform_method = "BEND"
    mod_curve.deform_axis = "X"
    mod_curve.angle = math.radians(15)

    smooth_subdiv(wing, 3)

    # Wing vein — thin cylinder running along the wing
    vein_loc = (origin[0] + length * 0.3, origin[1], origin[2] + 0.002)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.001, depth=length * 0.7, vertices=6, location=vein_loc
    )
    vein = bpy.context.active_object
    vein.name = f"{name}_Vein"
    vein.rotation_euler = (0, math.radians(90), math.radians(angle_z))
    bpy.ops.object.shade_smooth()

    return wing


# Forewings — larger
create_wing("Wing_Fore_L", (0.14, 0.06, 0.12), 0.42, 0.1, 22)
create_wing("Wing_Fore_R", (0.14, -0.06, 0.12), 0.42, 0.1, -22)

# Hindwings — smaller
create_wing("Wing_Hind_L", (0.05, 0.05, 0.11), 0.28, 0.07, 26)
create_wing("Wing_Hind_R", (0.05, -0.05, 0.11), 0.28, 0.07, -26)


# ══════════════════════════════════════════════════════════════════════
# LEGS — 3-segment jointed: coxa → femur → tibia
# ══════════════════════════════════════════════════════════════════════

def create_leg(pos_name, side, coxa_loc, angles):
    """Create a 3-segment jointed leg."""
    sign = 1 if side == "L" else -1
    coxa_rot, femur_rot, tibia_rot = angles

    # Coxa (short, thick — attaches to thorax)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.008, depth=0.06, vertices=8, location=coxa_loc
    )
    coxa = bpy.context.active_object
    coxa.name = f"Leg_{pos_name}_{side}_Coxa"
    coxa.rotation_euler = tuple(math.radians(r) for r in coxa_rot)
    bpy.ops.object.shade_smooth()

    # Femur (longer, thinner)
    fem_offset = Vector((0.02, 0.04 * sign, -0.05))
    fem_loc = Vector(coxa_loc) + fem_offset
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.006, depth=0.14, vertices=8, location=fem_loc
    )
    femur = bpy.context.active_object
    femur.name = f"Leg_{pos_name}_{side}_Femur"
    femur.rotation_euler = tuple(math.radians(r) for r in femur_rot)
    bpy.ops.object.shade_smooth()

    # Tibia (longest, thinnest — with slight taper)
    tib_offset = Vector((0.03, 0.06 * sign, -0.15))
    tib_loc = Vector(coxa_loc) + tib_offset
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.005, radius2=0.002, depth=0.18, vertices=8, location=tib_loc
    )
    tibia = bpy.context.active_object
    tibia.name = f"Leg_{pos_name}_{side}_Tibia"
    tibia.rotation_euler = tuple(math.radians(r) for r in tibia_rot)
    bpy.ops.object.shade_smooth()


# Front legs (angled forward)
create_leg("Fore", "L", (0.24, 0.1, -0.06),
    [(35, 0, 30), (15, 0, 35), (-20, 0, 20)])
create_leg("Fore", "R", (0.24, -0.1, -0.06),
    [(35, 0, -30), (15, 0, -35), (-20, 0, -20)])

# Mid legs (angled sideways)
create_leg("Mid", "L", (0.12, 0.12, -0.07),
    [(25, 0, 40), (10, 0, 42), (-15, 0, 22)])
create_leg("Mid", "R", (0.12, -0.12, -0.07),
    [(25, 0, -40), (10, 0, -42), (-15, 0, -22)])

# Hind legs (angled backward, longer)
create_leg("Hind", "L", (0.01, 0.11, -0.06),
    [(18, 0, 48), (8, 0, 48), (-10, 0, 18)])
create_leg("Hind", "R", (0.01, -0.11, -0.06),
    [(18, 0, -48), (8, 0, -48), (-10, 0, -18)])


# ══════════════════════════════════════════════════════════════════════
# ANTENNAE — elbowed, 3-segment: scape → pedicel → flagellum
# ══════════════════════════════════════════════════════════════════════
for side, y in [("L", 0.03), ("R", -0.03)]:
    sign = 1 if side == "L" else -1

    # Scape (thick base)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.007, depth=0.06, vertices=8,
        location=(0.47, y, 0.08)
    )
    scape = bpy.context.active_object
    scape.name = f"Antenna_{side}_Scape"
    scape.rotation_euler = (math.radians(-30), 0, math.radians(8 * sign))
    bpy.ops.object.shade_smooth()

    # Pedicel (elbow joint — small sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.008, segments=12, ring_count=8,
        location=(0.49, y * 1.3, 0.12)
    )
    pedicel = bpy.context.active_object
    pedicel.name = f"Antenna_{side}_Pedicel"
    bpy.ops.object.shade_smooth()

    # Flagellum (long whip)
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.005, radius2=0.002, depth=0.2, vertices=8,
        location=(0.52, y * 1.8, 0.2)
    )
    flag = bpy.context.active_object
    flag.name = f"Antenna_{side}_Flagellum"
    flag.rotation_euler = (math.radians(-55), 0, math.radians(15 * sign))
    bpy.ops.object.shade_smooth()


# ══════════════════════════════════════════════════════════════════════
# STINGER — prominent, sharp, menacing
# ══════════════════════════════════════════════════════════════════════
bpy.ops.mesh.primitive_cone_add(
    radius1=0.016, radius2=0.0008, depth=0.12, vertices=16,
    location=(-0.58, 0, -0.015)
)
stinger = bpy.context.active_object
stinger.name = "Stinger"
stinger.rotation_euler = (0, math.radians(92), 0)
smooth_subdiv(stinger, 2)


print("02_wasp_appendages.py V3 — jointed legs, curved wings with veins, elbowed antennae, stinger")
