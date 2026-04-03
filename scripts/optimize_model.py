"""Optimize the amber bee model for web delivery.
- Decimate geometry to reduce poly count
- Export as optimized GLB
- Report mesh stats before/after
"""

import bpy
import os
import sys

SOURCE = r"C:\Users\Brian\OneDrive\Desktop\Agentic Systems\vespid\source-model\source\model.glb"
OUTPUT = r"C:\Users\Brian\OneDrive\Desktop\Agentic Systems\vespid\wasp.glb"

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import the GLB
print(f"Loading: {SOURCE}")
bpy.ops.import_scene.gltf(filepath=SOURCE)

# Report what we imported
print("\n=== IMPORTED OBJECTS ===")
total_verts = 0
total_faces = 0
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        verts = len(obj.data.vertices)
        faces = len(obj.data.polygons)
        total_verts += verts
        total_faces += faces
        print(f"  {obj.name}: {verts:,} verts, {faces:,} faces")
    elif obj.type == 'ARMATURE':
        bones = len(obj.data.bones)
        print(f"  {obj.name}: ARMATURE ({bones} bones)")
    else:
        print(f"  {obj.name}: {obj.type}")

print(f"\nTOTAL: {total_verts:,} vertices, {total_faces:,} faces")

# Report animations
if bpy.data.actions:
    print(f"\n=== ANIMATIONS ({len(bpy.data.actions)}) ===")
    for action in bpy.data.actions:
        print(f"  {action.name}: frames {action.frame_range[0]:.0f}-{action.frame_range[1]:.0f}")

# Report materials
print(f"\n=== MATERIALS ({len(bpy.data.materials)}) ===")
for mat in bpy.data.materials:
    print(f"  {mat.name}")

# Decimate meshes that are too dense
DECIMATE_RATIO = 0.3  # Reduce to 30% of original poly count
print(f"\n=== DECIMATING (ratio={DECIMATE_RATIO}) ===")
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH':
        continue
    verts = len(obj.data.vertices)
    if verts > 5000:  # Only decimate dense meshes
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
        mod.ratio = DECIMATE_RATIO
        bpy.ops.object.modifier_apply(modifier="Decimate")
        new_verts = len(obj.data.vertices)
        print(f"  {obj.name}: {verts:,} → {new_verts:,} verts")
        obj.select_set(False)

# Report after
total_verts_after = 0
total_faces_after = 0
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        total_verts_after += len(obj.data.vertices)
        total_faces_after += len(obj.data.polygons)

print(f"\nAFTER: {total_verts_after:,} vertices, {total_faces_after:,} faces")
print(f"Reduction: {(1 - total_verts_after/max(total_verts,1))*100:.1f}%")

# Export optimized GLB
print(f"\nExporting to: {OUTPUT}")

kwargs = {
    "filepath": OUTPUT,
    "export_format": "GLB",
    "export_apply": True,
    "export_animations": True,
    "export_materials": "EXPORT",
    "export_skins": True,
    "check_existing": False,
}

# Adaptive param addition
optional = {
    "export_texcoords": True,
    "export_normals": True,
    "export_image_format": "AUTO",
    "export_animation_mode": "ACTIONS",
    "export_force_sampling": True,
    "export_def_bones": True,
    "use_visible": True,
    "use_active_scene": True,
}
for k, v in optional.items():
    kwargs[k] = v

max_attempts = 10
for attempt in range(max_attempts):
    try:
        bpy.ops.export_scene.gltf(**kwargs)
        break
    except TypeError as e:
        msg = str(e)
        if "unrecognized" in msg:
            bad_key = msg.split('"')[1] if '"' in msg else None
            if bad_key and bad_key in kwargs:
                print(f"  Removing unsupported param: {bad_key}")
                del kwargs[bad_key]
                continue
        raise

file_size = os.path.getsize(OUTPUT) / (1024 * 1024)
print(f"\nDone! Output size: {file_size:.1f} MB")
