"""Wasp materials V3 — realistic chitin with vertex color banding,
glossy compound eyes, translucent wings with vein hints.
"""

import bpy


# ══════════════════════════════════════════════════════════════════════
# CHITIN — dark exoskeleton, glossy like a real insect
# ══════════════════════════════════════════════════════════════════════
mat_chitin = bpy.data.materials.new(name="Chitin")
mat_chitin.use_nodes = True
nodes = mat_chitin.node_tree.nodes
links = mat_chitin.node_tree.links
bsdf = nodes.get("Principled BSDF")

# Dark brown-black chitin
bsdf.inputs["Base Color"].default_value = (0.04, 0.03, 0.015, 1.0)
bsdf.inputs["Roughness"].default_value = 0.22
bsdf.inputs["Specular IOR Level"].default_value = 0.75
bsdf.inputs["Metallic"].default_value = 0.05
# Slight clearcoat for that waxy chitin sheen
bsdf.inputs["Coat Weight"].default_value = 0.3
bsdf.inputs["Coat Roughness"].default_value = 0.15


# ══════════════════════════════════════════════════════════════════════
# ABDOMEN — uses vertex colors for black/yellow banding
# ══════════════════════════════════════════════════════════════════════
mat_abdomen = bpy.data.materials.new(name="AbdomenBanded")
mat_abdomen.use_nodes = True
nodes_a = mat_abdomen.node_tree.nodes
links_a = mat_abdomen.node_tree.links
bsdf_a = nodes_a.get("Principled BSDF")

# Add vertex color node
vcol_node = nodes_a.new("ShaderNodeVertexColor")
vcol_node.layer_name = "Col"

# Connect vertex colors to base color
links_a.new(vcol_node.outputs["Color"], bsdf_a.inputs["Base Color"])

bsdf_a.inputs["Roughness"].default_value = 0.25
bsdf_a.inputs["Specular IOR Level"].default_value = 0.7
bsdf_a.inputs["Metallic"].default_value = 0.03
bsdf_a.inputs["Coat Weight"].default_value = 0.25
bsdf_a.inputs["Coat Roughness"].default_value = 0.18


# ══════════════════════════════════════════════════════════════════════
# WING — translucent with iridescence
# ══════════════════════════════════════════════════════════════════════
mat_wing = bpy.data.materials.new(name="Wing")
mat_wing.use_nodes = True
bsdf_w = mat_wing.node_tree.nodes.get("Principled BSDF")

bsdf_w.inputs["Base Color"].default_value = (0.8, 0.82, 0.88, 1.0)
bsdf_w.inputs["Roughness"].default_value = 0.05
bsdf_w.inputs["Alpha"].default_value = 0.2
bsdf_w.inputs["Specular IOR Level"].default_value = 0.9
bsdf_w.inputs["Transmission Weight"].default_value = 0.6
bsdf_w.inputs["Coat Weight"].default_value = 0.5
bsdf_w.inputs["Coat Roughness"].default_value = 0.05
mat_wing.surface_render_method = "BLENDED"


# ══════════════════════════════════════════════════════════════════════
# COMPOUND EYE — near-black, very glossy, faceted look
# ══════════════════════════════════════════════════════════════════════
mat_eye = bpy.data.materials.new(name="CompoundEye")
mat_eye.use_nodes = True
bsdf_e = mat_eye.node_tree.nodes.get("Principled BSDF")

bsdf_e.inputs["Base Color"].default_value = (0.01, 0.008, 0.005, 1.0)
bsdf_e.inputs["Roughness"].default_value = 0.08
bsdf_e.inputs["Specular IOR Level"].default_value = 1.0
bsdf_e.inputs["Coat Weight"].default_value = 0.8
bsdf_e.inputs["Coat Roughness"].default_value = 0.02


# ══════════════════════════════════════════════════════════════════════
# STINGER — dark, metallic, menacing
# ══════════════════════════════════════════════════════════════════════
mat_stinger = bpy.data.materials.new(name="StingerMat")
mat_stinger.use_nodes = True
bsdf_s = mat_stinger.node_tree.nodes.get("Principled BSDF")

bsdf_s.inputs["Base Color"].default_value = (0.03, 0.02, 0.01, 1.0)
bsdf_s.inputs["Roughness"].default_value = 0.12
bsdf_s.inputs["Metallic"].default_value = 0.4
bsdf_s.inputs["Specular IOR Level"].default_value = 0.9


# ══════════════════════════════════════════════════════════════════════
# ASSIGN MATERIALS
# ══════════════════════════════════════════════════════════════════════
assignments = {
    "Chitin": [
        "Head", "Thorax", "Petiole", "Mandible_L", "Mandible_R",
        "Antenna_L_Scape", "Antenna_R_Scape",
        "Antenna_L_Flagellum", "Antenna_R_Flagellum",
    ],
    "AbdomenBanded": ["Abdomen"],
    "Wing": ["Wing_Fore_L", "Wing_Fore_R", "Wing_Hind_L", "Wing_Hind_R"],
    "CompoundEye": ["Eye_L", "Eye_R"],
    "StingerMat": ["Stinger"],
}

# Legs get chitin (3 segments)
for prefix in ["Fore", "Mid", "Hind"]:
    for side in ["L", "R"]:
        for part in ["Coxa", "Femur", "Tibia"]:
            assignments["Chitin"].append(f"Leg_{prefix}_{side}_{part}")

# Antenna pedicels get chitin
for side in ["L", "R"]:
    assignments["Chitin"].append(f"Antenna_{side}_Pedicel")

# Wing veins get chitin
for wtype in ["Fore", "Hind"]:
    for side in ["L", "R"]:
        assignments["Chitin"].append(f"Wing_{wtype}_{side}_Vein")

for mat_name, obj_names in assignments.items():
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        continue
    for obj_name in obj_names:
        obj = bpy.data.objects.get(obj_name)
        if obj and hasattr(obj, "data") and obj.data is not None:
            obj.data.materials.clear()
            obj.data.materials.append(mat)


print("03_wasp_materials.py complete — V3 chitin with clearcoat, banded abdomen, glossy eyes")
