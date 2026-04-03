"""Wasp animations: Idle, Agitated, Attack.
Blender 5.1 compatible — uses slotted action API with channelbags.
Each action is stashed to a named NLA track for GLTF multi-clip export.
"""

import bpy
import math
from bpy_extras import anim_utils


armature = bpy.data.objects.get("WaspArmature")
if not armature:
    raise RuntimeError("WaspArmature not found — run 04_wasp_rig.py first")

bpy.context.view_layer.objects.active = armature

# Ensure animation data exists
if armature.animation_data is None:
    armature.animation_data_create()


def create_action(name):
    """Create a new action with a slot and channelbag for Blender 5.1."""
    action = bpy.data.actions.new(name=name)
    slot = action.slots.new(id_type="OBJECT", name=armature.name)
    channelbag = anim_utils.action_ensure_channelbag_for_slot(action, slot)
    return action, slot, channelbag


def add_keyframes(channelbag, bone_name, channel, frames_values, index=0):
    """
    Add keyframes to a channelbag fcurve.

    bone_name: name of the pose bone
    channel: 'location', 'rotation_euler', 'scale', 'rotation_quaternion'
    frames_values: list of (frame, value) tuples
    index: channel index (0=X, 1=Y, 2=Z, 3=W for quaternion)
    """
    data_path = f'pose.bones["{bone_name}"].{channel}'
    fc = channelbag.fcurves.ensure(data_path, index=index, group_name=bone_name)
    for frame, value in frames_values:
        fc.keyframe_points.insert(frame, value)


def stash_to_nla(action, slot, track_name):
    """Push action to NLA track. Track name = Three.js clip name."""
    # Temporarily assign action + slot so NLA can reference it
    armature.animation_data.action = action
    armature.animation_data.action_slot = slot

    track = armature.animation_data.nla_tracks.new()
    track.name = track_name
    start = int(action.frame_range[0])
    strip = track.strips.new(action.name, start, action)
    strip.name = track_name

    # Clear active action after stashing
    armature.animation_data.action = None


# ══════════════════════════════════════════════════════════════════════
# IDLE — gentle bob, antennae twitch, abdomen breathing
# ══════════════════════════════════════════════════════════════════════
idle_action, idle_slot, idle_cb = create_action("Idle")

idle_frames = 72  # 3-second loop at 24fps

# Root: gentle vertical bob
for axis_idx in range(3):
    kfs = []
    for frame in range(0, idle_frames + 1, 6):
        t = frame / idle_frames
        if axis_idx == 2:  # Z axis
            val = math.sin(t * math.pi * 2) * 0.008
        else:
            val = 0.0
        kfs.append((frame, val))
    add_keyframes(idle_cb, "Root", "location", kfs, index=axis_idx)

# Antennae: subtle oscillation
for side in ["L", "R"]:
    bone_name = f"Antenna_{side}"
    phase = 0 if side == "L" else 1.5
    kfs_x = []
    for frame in range(0, idle_frames + 1, 8):
        t = frame / idle_frames
        val = math.sin(t * math.pi * 4 + phase) * 0.025
        kfs_x.append((frame, val))
    add_keyframes(idle_cb, bone_name, "rotation_euler", kfs_x, index=0)

# Abdomen: breathing (scale pulse)
for axis_idx in range(3):
    kfs = []
    for frame in range(0, idle_frames + 1, 6):
        t = frame / idle_frames
        val = 1.0 + math.sin(t * math.pi * 2) * 0.008
        kfs.append((frame, val))
    add_keyframes(idle_cb, "Abdomen", "scale", kfs, index=axis_idx)

stash_to_nla(idle_action, idle_slot, "Idle")
print("  Idle animation: 72 frames")


# ══════════════════════════════════════════════════════════════════════
# AGITATED — wing vibration, body rock, abdomen curl
# ══════════════════════════════════════════════════════════════════════
agitated_action, agitated_slot, agitated_cb = create_action("Agitated")

agitated_frames = 48  # 2-second loop

# Wing vibration (high frequency flutter)
for side in ["L", "R"]:
    sign = 1 if side == "L" else -1
    for wing_type in ["Fore", "Hind"]:
        bone_name = f"Wing_{wing_type}_{side}"
        amplitude = 0.12 if wing_type == "Fore" else 0.09
        kfs = []
        for frame in range(0, agitated_frames + 1, 2):
            t = frame / agitated_frames
            val = math.sin(t * math.pi * 24) * amplitude * sign
            kfs.append((frame, val))
        add_keyframes(agitated_cb, bone_name, "rotation_euler", kfs, index=0)

# Body rock (Root location)
for axis_idx in range(3):
    kfs = []
    for frame in range(0, agitated_frames + 1, 3):
        t = frame / agitated_frames
        if axis_idx == 0:  # X: forward-back rock
            val = math.sin(t * math.pi * 6) * 0.015
        elif axis_idx == 2:  # Z: vertical shake
            val = math.sin(t * math.pi * 8) * 0.01
        else:
            val = 0.0
        kfs.append((frame, val))
    add_keyframes(agitated_cb, "Root", "location", kfs, index=axis_idx)

# Abdomen curl (rotation on X)
kfs_abd = []
for frame in range(0, agitated_frames + 1, 3):
    t = frame / agitated_frames
    val = math.sin(t * math.pi * 3) * 0.08
    kfs_abd.append((frame, val))
add_keyframes(agitated_cb, "Abdomen", "rotation_euler", kfs_abd, index=0)

# Antennae: faster, wider movement
for side in ["L", "R"]:
    bone_name = f"Antenna_{side}"
    phase = 0 if side == "L" else 2.0
    kfs = []
    for frame in range(0, agitated_frames + 1, 3):
        t = frame / agitated_frames
        val = math.sin(t * math.pi * 8 + phase) * 0.06
        kfs.append((frame, val))
    add_keyframes(agitated_cb, bone_name, "rotation_euler", kfs, index=0)

stash_to_nla(agitated_action, agitated_slot, "Agitated")
print("  Agitated animation: 48 frames")


# ══════════════════════════════════════════════════════════════════════
# ATTACK — lunge, stinger extend, wing blur
# ══════════════════════════════════════════════════════════════════════
attack_action, attack_slot, attack_cb = create_action("Attack")

attack_frames = 36  # 1.5-second loop

# Root: lunge forward then return
lunge_kfs_x = [
    (0, 0.0),
    (6, 0.03),       # Wind up
    (12, -0.08),     # Lunge forward
    (18, -0.06),     # Hold
    (30, 0.0),       # Return
    (36, 0.0),
]
lunge_kfs_z = [
    (0, 0.0),
    (6, 0.015),      # Rise slightly
    (12, -0.01),     # Dip on lunge
    (18, -0.005),
    (30, 0.0),
    (36, 0.0),
]
add_keyframes(attack_cb, "Root", "location", lunge_kfs_x, index=0)
add_keyframes(attack_cb, "Root", "location", [(f, 0) for f, _ in lunge_kfs_x], index=1)
add_keyframes(attack_cb, "Root", "location", lunge_kfs_z, index=2)

# Stinger: thrust out and retract
stinger_kfs = [
    (0, 0.0),
    (10, 0.0),
    (12, -0.05),     # Thrust
    (20, -0.05),     # Hold
    (28, 0.0),       # Retract
    (36, 0.0),
]
add_keyframes(attack_cb, "Stinger", "location", stinger_kfs, index=0)
add_keyframes(attack_cb, "Stinger", "location", [(f, 0) for f, _ in stinger_kfs], index=1)

# Abdomen: curl down during sting
abd_attack_kfs = [
    (0, 0.0),
    (8, 0.0),
    (12, 0.12),      # Curl under
    (20, 0.12),      # Hold
    (28, 0.0),       # Return
    (36, 0.0),
]
add_keyframes(attack_cb, "Abdomen", "rotation_euler", abd_attack_kfs, index=0)

# Wings: constant fast vibration
for side in ["L", "R"]:
    sign = 1 if side == "L" else -1
    for wing_type in ["Fore", "Hind"]:
        bone_name = f"Wing_{wing_type}_{side}"
        amplitude = 0.18 if wing_type == "Fore" else 0.14
        kfs = []
        for frame in range(0, attack_frames + 1, 1):
            t = frame / attack_frames
            val = math.sin(t * math.pi * 36) * amplitude * sign
            kfs.append((frame, val))
        add_keyframes(attack_cb, bone_name, "rotation_euler", kfs, index=0)

# Head: slight forward thrust during attack
head_kfs = [
    (0, 0.0),
    (10, 0.0),
    (12, -0.015),    # Forward
    (20, -0.01),
    (30, 0.0),
    (36, 0.0),
]
add_keyframes(attack_cb, "Head", "location", head_kfs, index=0)
add_keyframes(attack_cb, "Head", "location", [(f, 0) for f, _ in head_kfs], index=1)
add_keyframes(attack_cb, "Head", "location", [(f, 0) for f, _ in head_kfs], index=2)

stash_to_nla(attack_action, attack_slot, "Attack")
print("  Attack animation: 36 frames")


print("05_wasp_animate.py complete — 3 animations stashed to NLA (Idle, Agitated, Attack)")
