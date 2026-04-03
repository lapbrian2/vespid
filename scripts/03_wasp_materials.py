"""Wasp materials: chitin (black), yellow bands, translucent wings, compound eyes."""

import bpy


# ── CHITIN (dark exoskeleton) ─────────────────────────────────────────
mat_chitin = bpy.data.materials.new(name="Chitin")
mat_chitin.use_nodes = True
bsdf = mat_chitin.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (0.05, 0.04, 0.02, 1.0)
bsdf.inputs["Roughness"].default_value = 0.28
bsdf.inputs["Specular IOR Level"].default_value = 0.65


# ── YELLOW BAND ───────────────────────────────────────────────────────
mat_yellow = bpy.data.materials.new(name="YellowBand")
mat_yellow.use_nodes = True
bsdf_y = mat_yellow.node_tree.nodes.get("Principled BSDF")
bsdf_y.inputs["Base Color"].default_value = (0.9, 0.72, 0.08, 1.0)
bsdf_y.inputs["Roughness"].default_value = 0.32
bsdf_y.inputs["Specular IOR Level"].default_value = 0.5


# ── WING (translucent, iridescent) ───────────────────────────────────
mat_wing = bpy.data.materials.new(name="Wing")
mat_wing.use_nodes = True
bsdf_w = mat_wing.node_tree.nodes.get("Principled BSDF")
bsdf_w.inputs["Base Color"].default_value = (0.75, 0.78, 0.85, 1.0)
bsdf_w.inputs["Roughness"].default_value = 0.08
bsdf_w.inputs["Alpha"].default_value = 0.25
bsdf_w.inputs["Specular IOR Level"].default_value = 0.85
# Enable alpha blending for EEVEE
mat_wing.surface_render_method = "BLENDED"


# ── COMPOUND EYE (dark, glossy) ───────────────────────────────────────
mat_eye = bpy.data.materials.new(name="CompoundEye")
mat_eye.use_nodes = True
bsdf_e = mat_eye.node_tree.nodes.get("Principled BSDF")
bsdf_e.inputs["Base Color"].default_value = (0.015, 0.012, 0.01, 1.0)
bsdf_e.inputs["Roughness"].default_value = 0.12
bsdf_e.inputs["Specular IOR Level"].default_value = 0.95


# ── STINGER (dark metallic) ───────────────────────────────────────────
mat_stinger = bpy.data.materials.new(name="StingerMat")
mat_stinger.use_nodes = True
bsdf_s = mat_stinger.node_tree.nodes.get("Principled BSDF")
bsdf_s.inputs["Base Color"].default_value = (0.04, 0.03, 0.02, 1.0)
bsdf_s.inputs["Roughness"].default_value = 0.18
bsdf_s.inputs["Metallic"].default_value = 0.3
bsdf_s.inputs["Specular IOR Level"].default_value = 0.8


# ── ASSIGN MATERIALS ──────────────────────────────────────────────────
assignments = {
    "Chitin": [
        "Head", "Thorax", "Petiole", "Mandible_L", "Mandible_R",
        "Antenna_L_Scape", "Antenna_R_Scape",
        "Antenna_L_Flagellum", "Antenna_R_Flagellum",
    ],
    "YellowBand": ["Abdomen"],
    "Wing": ["Wing_Fore_L", "Wing_Fore_R", "Wing_Hind_L", "Wing_Hind_R"],
    "CompoundEye": ["Eye_L", "Eye_R"],
    "StingerMat": ["Stinger"],
}

# Legs get chitin
for prefix in ["Fore", "Mid", "Hind"]:
    for side in ["L", "R"]:
        for part in ["Femur", "Tibia"]:
            assignments["Chitin"].append(f"Leg_{prefix}_{side}_{part}")

for mat_name, obj_names in assignments.items():
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        continue
    for obj_name in obj_names:
        obj = bpy.data.objects.get(obj_name)
        if obj and hasattr(obj, "data") and obj.data is not None:
            obj.data.materials.clear()
            obj.data.materials.append(mat)


print("03_wasp_materials.py complete — Chitin, YellowBand, Wing, CompoundEye, Stinger materials assigned")
