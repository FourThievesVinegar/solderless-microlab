import cadquery as cq
import sys

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

helix_radius = 36.0
helix_pitch = 12.0
helix_height = 126.0
outer_tube_radius = 5.0
inner_tube_radius = 4.0

print("Test 1: Create helix wire")
try:
    helix_wire = cq.Wire.makeHelix(helix_pitch, helix_height, helix_radius)
    print("✓ Helix created")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

print("\nTest 2: Create ring cross-section")
try:
    ring = (
        cq.Workplane("XZ")
            .center(helix_radius, 0)
            .circle(inner_tube_radius)
            .circle(outer_tube_radius)
    )
    print("✓ Ring created")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

print("\nTest 3: Sweep ring along helix (isFrenet=True)")
try:
    tube = ring.sweep(helix_wire, multisection=False, isFrenet=True)
    print("✓ Sweep succeeded")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

print("\nTest 4: show_object(tube)")
try:
    show_object(tube)
    print("✓ show_object succeeded")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

print("\nAll tests passed!")
print(f"Tube type: {type(tube)}")
print(f"Tube solid: {tube.val()}")
