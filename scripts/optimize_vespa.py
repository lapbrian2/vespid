"""Import, optimize, and SEPARATE WINGS from the Vespa Orientalis model.
Strategy: separate by loose parts, then recombine small fragments back into body,
keeping only the largest flat pieces as wings.
"""

import bpy
import os

SOURCE = r"C:\Users\Brian\OneDrive\Desktop\Agentic Systems\vespid\vespa-model\source\II_ Calabrone Orientale.glb"
OUTPUT = r"C:\Users\Brian\OneDrive\Desktop\Agentic Systems\vespid\wasp.glb"

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print(f"Loading: {SOURCE}")
bpy.ops.import_scene.gltf(filepath=SOURCE)

# Get the main large meshes
all_meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
all_meshes.sort(key=lambda o: len(o.data.vertices), reverse=True)
print(f"\nMeshes: {len(all_meshes)}")
for m in all_meshes:
    print(f"  {m.name}: {len(m.data.vertices):,} verts")

# The biggest mesh is the body — separate it
main = all_meshes[0]
print(f"\nSeparating {main.name} by loose parts...")
bpy.ops.object.select_all(action='DESELECT')
main.select_set(True)
bpy.context.view_layer.objects.active = main
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

# Now analyze all fragments
fragments = [o for o in bpy.context.scene.objects if o.type == 'MESH']
fragments.sort(key=lambda o: len(o.data.vertices), reverse=True)

print(f"\n=== {len(fragments)} fragments ===")

# Classify: wings are flat pieces (high aspect ratio) with 400-2000 verts
# positioned above the body center
wings = []
body_parts = []

for obj in fragments:
    verts = len(obj.data.vertices)
    dims = obj.dimensions
    z_thickness = min(dims.x, dims.y, dims.z)
    max_spread = max(dims.x, dims.y, dims.z)

    if z_thickness < 0.001:
        body_parts.append(obj)
        continue

    aspect = max_spread / z_thickness

    # Wing criteria: 200-2000 verts, flat (aspect > 5), spread > 0.15
    is_wing = (200 <= verts <= 2000 and aspect > 5 and max_spread > 0.15)

    if is_wing and len(wings) < 4:  # Max 4 wings
        wings.append(obj)
        print(f"  WING: {obj.name} ({verts} verts, aspect {aspect:.1f}, spread {max_spread:.3f})")
    else:
        body_parts.append(obj)

print(f"\nFound {len(wings)} wings, {len(body_parts)} body parts")

# Name the wings based on position
# Sort by Y position to distinguish left/right
wings.sort(key=lambda w: w.location.y)
wing_names = []
if len(wings) >= 2:
    # At minimum: one right, one left
    wings[0].name = "Wing_R"
    wing_names.append("Wing_R")
    wings[-1].name = "Wing_L"
    wing_names.append("Wing_L")
if len(wings) >= 4:
    wings[1].name = "Wing_Hind_R"
    wing_names.append("Wing_Hind_R")
    wings[2].name = "Wing_Hind_L"
    wing_names.append("Wing_Hind_L")
elif len(wings) == 3:
    wings[1].name = "Wing_Mid"
    wing_names.append("Wing_Mid")

print(f"Wing names: {wing_names}")

# Join all body parts back into one mesh called "Body"
if len(body_parts) > 1:
    print(f"\nJoining {len(body_parts)} body fragments...")
    bpy.ops.object.select_all(action='DESELECT')
    for bp in body_parts:
        bp.select_set(True)
    bpy.context.view_layer.objects.active = body_parts[0]
    bpy.ops.object.join()
    body = bpy.context.active_object
    body.name = "Body"
    print(f"  Body: {len(body.data.vertices):,} verts")

# Decimate
RATIO = 0.18
print(f"\n=== DECIMATING (ratio={RATIO}) ===")
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH':
        continue
    verts = len(obj.data.vertices)
    if verts > 1000:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        mod = obj.modifiers.new(name="Dec", type='DECIMATE')
        mod.ratio = RATIO
        bpy.ops.object.modifier_apply(modifier="Dec")
        print(f"  {obj.name}: {verts:,} → {len(obj.data.vertices):,}")

# Resize textures
MAX_TEX = 1024
for img in bpy.data.images:
    if img.size[0] > MAX_TEX or img.size[1] > MAX_TEX:
        img.scale(min(img.size[0], MAX_TEX), min(img.size[1], MAX_TEX))

# Final
print("\n=== FINAL ===")
for obj in sorted(bpy.context.scene.objects, key=lambda o: o.name):
    if obj.type == 'MESH':
        print(f"  {obj.name}: {len(obj.data.vertices):,} verts")

# Export
print(f"\nExporting...")
kwargs = {
    "filepath": OUTPUT, "export_format": "GLB", "export_apply": True,
    "export_materials": "EXPORT", "export_image_format": "AUTO",
    "check_existing": False, "export_texcoords": True, "export_normals": True,
    "use_visible": True, "use_active_scene": True,
}
for attempt in range(10):
    try:
        bpy.ops.export_scene.gltf(**kwargs)
        break
    except TypeError as e:
        msg = str(e)
        if "unrecognized" in msg:
            bad = msg.split('"')[1] if '"' in msg else None
            if bad and bad in kwargs: del kwargs[bad]; continue
        raise

print(f"Done! {os.path.getsize(OUTPUT)/(1024*1024):.1f} MB")
