"""Import, analyze, decimate, and export the Vespa Orientalis model for web."""

import bpy
import os

SOURCE = r"C:\Users\Brian\OneDrive\Desktop\Agentic Systems\vespid\vespa-model\source\II_ Calabrone Orientale.glb"
OUTPUT = r"C:\Users\Brian\OneDrive\Desktop\Agentic Systems\vespid\wasp.glb"

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import
print(f"Loading: {SOURCE}")
bpy.ops.import_scene.gltf(filepath=SOURCE)

# Report
print("\n=== IMPORTED OBJECTS ===")
total_verts = 0
total_faces = 0
mesh_objects = []
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        verts = len(obj.data.vertices)
        faces = len(obj.data.polygons)
        total_verts += verts
        total_faces += faces
        mesh_objects.append(obj)
        print(f"  {obj.name}: {verts:,} verts, {faces:,} faces, mats: {[m.name for m in obj.data.materials if m]}")
    elif obj.type == 'ARMATURE':
        print(f"  {obj.name}: ARMATURE ({len(obj.data.bones)} bones)")
    elif obj.type == 'EMPTY':
        print(f"  {obj.name}: EMPTY (children: {len(obj.children)})")
    else:
        print(f"  {obj.name}: {obj.type}")

print(f"\nTOTAL: {total_verts:,} verts, {total_faces:,} faces, {len(mesh_objects)} mesh objects")

# Animations
if bpy.data.actions:
    print(f"\n=== ANIMATIONS ({len(bpy.data.actions)}) ===")
    for action in bpy.data.actions:
        print(f"  {action.name}: frames {action.frame_range[0]:.0f}-{action.frame_range[1]:.0f}")
else:
    print("\n=== NO ANIMATIONS ===")

# Materials
print(f"\n=== MATERIALS ({len(bpy.data.materials)}) ===")
for mat in bpy.data.materials:
    print(f"  {mat.name}")

# Images
print(f"\n=== IMAGES ({len(bpy.data.images)}) ===")
for img in bpy.data.images:
    print(f"  {img.name}: {img.size[0]}x{img.size[1]} packed={img.packed_file is not None}")

# Decimate heavy meshes more aggressively for web
DECIMATE_RATIO = 0.15  # 15% of original — aggressive for web
print(f"\n=== DECIMATING (ratio={DECIMATE_RATIO}) ===")
for obj in mesh_objects:
    verts = len(obj.data.vertices)
    if verts > 1000:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
        mod.ratio = DECIMATE_RATIO
        bpy.ops.object.modifier_apply(modifier="Decimate")
        new_verts = len(obj.data.vertices)
        print(f"  {obj.name}: {verts:,} → {new_verts:,} verts")

# Resize textures if too large
print("\n=== RESIZING TEXTURES ===")
MAX_TEX_SIZE = 1024
for img in bpy.data.images:
    if img.size[0] > MAX_TEX_SIZE or img.size[1] > MAX_TEX_SIZE:
        old_size = f"{img.size[0]}x{img.size[1]}"
        img.scale(min(img.size[0], MAX_TEX_SIZE), min(img.size[1], MAX_TEX_SIZE))
        print(f"  {img.name}: {old_size} → {img.size[0]}x{img.size[1]}")

# Report after
total_verts_after = sum(len(o.data.vertices) for o in bpy.context.scene.objects if o.type == 'MESH')
print(f"\nAFTER: {total_verts_after:,} vertices")
print(f"Reduction: {(1 - total_verts_after/max(total_verts,1))*100:.1f}%")

# Export
print(f"\nExporting to: {OUTPUT}")
kwargs = {
    "filepath": OUTPUT,
    "export_format": "GLB",
    "export_apply": True,
    "export_animations": True,
    "export_materials": "EXPORT",
    "export_image_format": "AUTO",
    "export_skins": True,
    "check_existing": False,
    "export_texcoords": True,
    "export_normals": True,
    "use_visible": True,
    "use_active_scene": True,
}

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
                del kwargs[bad_key]
                continue
        raise

file_size = os.path.getsize(OUTPUT) / (1024 * 1024)
print(f"\nDone! Output: {file_size:.1f} MB")
