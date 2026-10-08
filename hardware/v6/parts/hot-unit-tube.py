import cadquery as cq
import math

if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

helix_radius = 36.0
helix_pitch = 12.0
helix_height = 126.0
outer_tube_radius = 5.0
inner_tube_radius = 4.0
bending_radius = 14.0
straight_length = 100.0

# Helix
helix_wire = (
    cq.Wire.makeHelix(helix_pitch, helix_height, helix_radius)
)

ring = (
    cq.Workplane("XZ")
        .center(helix_radius, 0)
        .circle(inner_tube_radius)
        .circle(outer_tube_radius)
)

# Upper-left bend
end_point = helix_wire.Vertices()[-1].toTuple()

upper_left_bend_wire = (
    cq.Wire.makeEllipse(
        x_radius=bending_radius,
        y_radius=bending_radius,
        center=(end_point[0], end_point[1], end_point[2]+bending_radius),
        normal=(1, 0, 0),
        xDir=(0, 0, 1),
        angle1=90,
        angle2=180,
        closed=False
    )
)

# Upper straight part
upper_left_straight_wire = (
    cq.Edge.makeLine(
        (
            end_point[0], 
            end_point[1] - bending_radius, 
            end_point[2] + bending_radius
        ),
        (
            end_point[0], 
            end_point[1] - bending_radius, 
            end_point[2] + bending_radius + straight_length
        )
    )
)

# Lower bends

lower_bend_side_wire = (
    cq.Wire.makeEllipse(
        x_radius=bending_radius,
        y_radius=bending_radius,
        center=(helix_radius - bending_radius, 0, 0),
        normal=(0, 0, 1),
        xDir=(0, 1, 0),
        angle1=180,
        angle2=270,
        closed=False
    )
)

lower_bend_up_wire = (
    cq.Wire.makeEllipse(
        x_radius=bending_radius,
        y_radius=bending_radius,
        center=(helix_radius - bending_radius, -bending_radius, bending_radius),
        normal=(0, 1, 0),
        xDir=(1, 0, 0),
        angle1=90,
        angle2=180,
        closed=False
    )
)

# Lower straight part
"""
lower_straight_wire = (
    cq.Edge.makeLine(
        (
            helix_radius - 2*bending_radius, 
            -bending_radius, 
            bending_radius
        ),
        (
            helix_radius - 2*bending_radius, 
            -bending_radius, 
            bending_radius + helix_height + straight_length
        )
    )
)
"""

# Replace lower_straight_wire with a Bezier (B-spline) curve
lower_straight_start = (
    helix_radius - 2 * bending_radius,
    -bending_radius,
    bending_radius
)
lower_straight_end = (
    helix_radius - 2 * bending_radius + 10,  # 10 mm shift in X
    -bending_radius,
    bending_radius + helix_height + straight_length
)

# Define control points for a gentle rightward Bezier curve
bezier_control_points = [
    cq.Vector(*lower_straight_start),
    cq.Vector(lower_straight_start[0] + 7, lower_straight_start[1], lower_straight_start[2] + (helix_height + straight_length) * 0.33),
    cq.Vector(lower_straight_start[0] + 10, lower_straight_start[1], lower_straight_start[2] + (helix_height + straight_length) * 0.66),
    cq.Vector(*lower_straight_end)
]

lower_straight_wire = cq.Edge.makeSpline(bezier_control_points)

# Combining

whole_wire = (cq.Wire.combine([
    helix_wire, 
    upper_left_bend_wire, 
    upper_left_straight_wire,
    lower_bend_side_wire,
    lower_bend_up_wire,
    lower_straight_wire
    ])
)

tube = ring.sweep(whole_wire[0], multisection=False, isFrenet=True)

show_object(tube)