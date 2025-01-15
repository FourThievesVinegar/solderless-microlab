import cadquery as cq

outer_diameter = 67.0
inner_diameter = 52.0
mason_thread_od = 61.0
thread_pitch = 3.5
thread_h = thread_pitch * 2.5
lid_h = thread_h + 2
wall_thickness = 1
thread_contour_diam = 2.1

thread_r = mason_thread_od/2 + thread_contour_diam 

# Helix
helix_wire = cq.Wire.makeHelix(pitch=thread_pitch, height=thread_h, radius=thread_r)
helix = cq.Workplane(obj=helix_wire)
#show_object(helix)

# Final result. A circle sweeped along a helix.
threads = (
    cq.Workplane('XZ')
    .center(thread_r, 0)
    .circle(thread_contour_diam/2)
    .sweep(helix_wire, isFrenet=True)
)
#show_object(threads)

mason_thread = (cq
    .Workplane("XY")
    .circle(thread_r + wall_thickness)
    .circle(thread_r)
    .extrude(lid_h)
)

import cadquery as cq

# Create the flat ring by subtracting inner hole from outer shape
flat_ring = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)  # Outer boundary
    .circle(inner_diameter / 2)  # Inner cutout
    .extrude(wall_thickness)  # Define thickness
)

mason_thread = mason_thread.union(flat_ring)
mason_thread = mason_thread.union(threads).faces("XY").workplane(origin=(0,0,0)).split(1,0)

show_object(mason_thread)