#!/usr/bin/env python3
"""Master build script - runs all wasp generation steps in Blender.
Run with: blender --background --python build_wasp.py
"""

import bpy
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.dirname(SCRIPT_DIR)


def run_script(filename):
    filepath = os.path.join(SCRIPT_DIR, filename)
    print(f"\n{'=' * 60}")
    print(f"Running: {filename}")
    print(f"{'=' * 60}")
    with open(filepath, "r") as f:
        exec(f.read(), {"__file__": filepath, "__name__": "__main__"})


# Clear default scene
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Run pipeline
run_script("01_wasp_body.py")
run_script("02_wasp_appendages.py")
run_script("03_wasp_materials.py")
run_script("04_wasp_rig.py")
run_script("05_wasp_animate.py")
run_script("06_wasp_export.py")

print(f"\nBuild complete! Model exported to: {OUTPUT_DIR}/wasp.glb")
