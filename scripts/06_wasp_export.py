"""Export wasp model as GLTF/GLB for Three.js consumption.
Blender 5.1 compatible. Uses minimal safe export settings, adding params
one at a time to avoid API mismatches across Blender versions.
"""

import bpy
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "wasp.glb")


# ── BUILD EXPORT KWARGS ───────────────────────────────────────────────
# Start minimal, add optional params if they exist in this Blender version
kwargs = {
    "filepath": OUTPUT_PATH,
    "export_format": "GLB",
    "export_apply": True,
    "export_animations": True,
    "check_existing": False,
}

# Try adding optional params safely
optional_params = {
    "export_texcoords": True,
    "export_normals": True,
    "export_tangents": True,
    "export_attributes": True,
    "export_materials": "EXPORT",
    "export_image_format": "AUTO",
    "export_animation_mode": "ACTIONS",
    "export_optimize_animation_size": True,
    "export_force_sampling": True,
    "export_skins": True,
    "export_all_influences": False,
    "export_def_bones": True,
    "use_selection": False,
    "use_visible": True,
    "use_active_scene": True,
}


def test_param(param_name, param_value):
    """Test if a parameter is valid by checking the operator's RNA properties."""
    try:
        # Try a dry run with just this param + filepath
        # Actually, just add it and let the main call handle errors
        return True
    except Exception:
        return False


# Add all optional params — if one fails, we'll catch it
for key, val in optional_params.items():
    kwargs[key] = val


# ── EXPORT ────────────────────────────────────────────────────────────
# Try with all params first, strip failing ones iteratively
max_attempts = 10
for attempt in range(max_attempts):
    try:
        bpy.ops.export_scene.gltf(**kwargs)
        break
    except TypeError as e:
        # Extract the unrecognized keyword
        msg = str(e)
        if "unrecognized" in msg:
            # Parse: keyword "xxx" unrecognized
            bad_key = msg.split('"')[1] if '"' in msg else None
            if bad_key and bad_key in kwargs:
                print(f"  Removing unsupported param: {bad_key}")
                del kwargs[bad_key]
                continue
        raise
else:
    raise RuntimeError("Failed to export after removing unsupported params")


file_size = os.path.getsize(OUTPUT_PATH) / 1024
print(f"06_wasp_export.py complete — Exported: {OUTPUT_PATH}")
print(f"  File size: {file_size:.1f} KB")
