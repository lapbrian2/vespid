"""Wasp armature rig with vertex-group-based mesh parenting.
Blender 5.1 compatible. Uses auto-weights for GLTF-compatible skinning.
"""

import bpy
import mathutils


# ── CREATE ARMATURE ───────────────────────────────────────────────────
arm_data = bpy.data.armatures.new("WaspRig")
arm_obj = bpy.data.objects.new("WaspArmature", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj

bpy.ops.object.mode_set(mode="EDIT")
edit_bones = arm_data.edit_bones


# ── BONE DEFINITIONS ──────────────────────────────────────────────────
# Each bone: (name, head, tail, parent_name, connected, deform)
bone_defs = [
    # Core chain
    ("Root",    (0, 0, 0),        (0, 0, 0.1),      None,       False, True),
    ("Thorax",  (0.15, 0, 0),     (0.15, 0, 0.15),   "Root",     False, True),
    ("Head",    (0.55, 0, 0.05),  (0.55, 0, 0.18),   "Thorax",   False, True),
    ("Petiole", (-0.05, 0, -0.01),(-0.2, 0, -0.02),  "Thorax",   False, True),
    ("Abdomen", (-0.25, 0, -0.03),(-0.65, 0, -0.04), "Petiole",  False, True),
    ("Stinger", (-0.65, 0, -0.04),(-0.85, 0, -0.05), "Abdomen",  False, True),

    # Wings (4 bones)
    ("Wing_Fore_L", (0.18, 0.08, 0.16),  (0.18, 0.5, 0.25),  "Thorax", False, True),
    ("Wing_Fore_R", (0.18, -0.08, 0.16), (0.18, -0.5, 0.25), "Thorax", False, True),
    ("Wing_Hind_L", (0.06, 0.07, 0.15),  (0.06, 0.4, 0.22),  "Thorax", False, True),
    ("Wing_Hind_R", (0.06, -0.07, 0.15), (0.06, -0.4, 0.22), "Thorax", False, True),

    # Antennae (2 bones)
    ("Antenna_L", (0.6, 0.04, 0.13),  (0.7, 0.08, 0.28),  "Head", False, True),
    ("Antenna_R", (0.6, -0.04, 0.13), (0.7, -0.08, 0.28), "Head", False, True),
]

# Create all bones
for name, head, tail, parent_name, connected, deform in bone_defs:
    bone = edit_bones.new(name)
    bone.head = mathutils.Vector(head)
    bone.tail = mathutils.Vector(tail)
    bone.use_deform = deform
    bone.use_connect = connected
    if parent_name:
        bone.parent = edit_bones[parent_name]

bpy.ops.object.mode_set(mode="OBJECT")


# ── PARENT MESHES TO ARMATURE ─────────────────────────────────────────
# Map each mesh to the bone that should control it.
# Using direct bone parenting (rigid attachment) since these are separate
# mechanical parts, not a deformable skin mesh.

bone_mesh_map = {
    "Head":         ["Head", "Mandible_L", "Mandible_R", "Eye_L", "Eye_R"],
    "Thorax":       ["Thorax"],
    "Petiole":      ["Petiole"],
    "Abdomen":      ["Abdomen"],
    "Stinger":      ["Stinger"],
    "Wing_Fore_L":  ["Wing_Fore_L"],
    "Wing_Fore_R":  ["Wing_Fore_R"],
    "Wing_Hind_L":  ["Wing_Hind_L"],
    "Wing_Hind_R":  ["Wing_Hind_R"],
    "Antenna_L":    ["Antenna_L_Scape", "Antenna_L_Flagellum"],
    "Antenna_R":    ["Antenna_R_Scape", "Antenna_R_Flagellum"],
}

# Add legs to Thorax (3 segments now: coxa, femur, tibia)
for prefix in ["Fore", "Mid", "Hind"]:
    for side in ["L", "R"]:
        for part in ["Coxa", "Femur", "Tibia"]:
            bone_mesh_map.setdefault("Thorax", []).append(f"Leg_{prefix}_{side}_{part}")

# Add wing veins to wing bones
for wtype in ["Fore", "Hind"]:
    for side in ["L", "R"]:
        vein_name = f"Wing_{wtype}_{side}_Vein"
        bone_mesh_map.setdefault(f"Wing_{wtype}_{side}", []).append(vein_name)

# Add antenna pedicels to antenna bones
for side in ["L", "R"]:
    bone_mesh_map.setdefault(f"Antenna_{side}", []).append(f"Antenna_{side}_Pedicel")

for bone_name, mesh_names in bone_mesh_map.items():
    for mesh_name in mesh_names:
        obj = bpy.data.objects.get(mesh_name)
        if not obj:
            print(f"  WARNING: Mesh '{mesh_name}' not found, skipping")
            continue

        # Parent to bone (rigid)
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        arm_obj.select_set(True)
        bpy.context.view_layer.objects.active = arm_obj
        arm_obj.data.bones.active = arm_obj.data.bones[bone_name]
        bpy.ops.object.parent_set(type="BONE")


# ── APPLY TRANSFORMS ──────────────────────────────────────────────────
# Critical for GLTF export: unapplied transforms cause warped meshes
all_objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
all_objects.append(arm_obj)

for obj in all_objects:
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


print("04_wasp_rig.py complete — Armature with 12 bones, meshes parented, transforms applied")
