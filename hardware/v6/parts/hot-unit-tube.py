"""Copper heat exchanger coil of the heating unit (TC-CTB).

APPROXIMATION: the builder bends this by hand (docs/assembly-temperature-
exchangers-unit.md), so it has no fixed shape. As in cold-unit-tube.py, one
end drops inside the coil to the bottom and the tube winds back up as a helix
to the other lid hole.

- Tube: 1/4 in OD x 3/16 in ID, from the parts list.
- Frame: the lid's. The holes are at x = +-24 mm, the lid's top face is z = 0
  and the jar is towards +z; its inside bottom is at z = 236.
- The immersion heater (hot-unit-heater) hangs from the lid's pocket down to
  z = 121. The down-leg drops straight from its hole past it, and the coil
  (44 mm radius) winds below it, from z = 130, about 14 mm from the heater
  and 6 mm from the jar.
- turns must be a whole number plus a half so that the coil ends under the
  second hole. Other values are guesses.
"""

import cadquery as cq

if "show_object" not in globals():
    def show_object(*args, **kwargs):
        pass

tube_od = 6.35
tube_id = 4.7625
hole_x = 24.0
stick_out = 40.0
bend_z = 15.0
coil_radius = 44.0
turns = 5.5
coil_top = 130.0
coil_bottom = 222.0
# Distance of the down-leg from the axis inside the coil.
leg_x = 24.0

down = cq.Vector(0, 0, 1)
up = cq.Vector(0, 0, -1)


def sweep(edge, frenet=False):
    p = edge.startPoint()
    t = edge.tangentAt(0)
    side = cq.Vector(0, 0, 1) if abs(t.z) < 0.9 else cq.Vector(1, 0, 0)
    plane = cq.Plane(origin=p, xDir=t.cross(side).normalized(), normal=t)
    return (
        cq.Workplane(plane)
        .circle(tube_od / 2)
        .circle(tube_id / 2)
        .sweep(cq.Workplane(obj=cq.Wire.assembleEdges([edge])), isFrenet=frenet)
        .val()
    )


def bend(p0, t0, p3, t3, d):
    return cq.Edge.makeBezier([p0, p0 + t0 * d, p3 - t3 * d, p3])


# The helix starts at (-coil_radius, 0, coil_bottom) and ends at
# (coil_radius, 0, coil_top).
helix = cq.Wire.makeHelix(
    pitch=(coil_bottom - coil_top) / turns,
    height=coil_bottom - coil_top,
    radius=coil_radius,
    center=cq.Vector(0, 0, coil_bottom),
    dir=up,
).Edges()[0]

leg_top = cq.Vector(-hole_x, 0, -stick_out)
leg_bend = cq.Vector(-hole_x, 0, bend_z)
inner_top = cq.Vector(-leg_x, 0, bend_z + 25)
inner_bottom = cq.Vector(-leg_x, 0, coil_bottom - 15)
riser_bend = cq.Vector(hole_x, 0, bend_z)
riser_top = cq.Vector(hole_x, 0, -stick_out)

edges = [
    (cq.Edge.makeLine(leg_top, leg_bend), False),
    (bend(leg_bend, down, inner_top, down, 12), False),
    (cq.Edge.makeLine(inner_top, inner_bottom), False),
    (bend(inner_bottom, down, helix.startPoint(), helix.tangentAt(0), 15), False),
    (helix, True),
    (bend(helix.endPoint(), helix.tangentAt(1), riser_bend, up, 15), False),
    (cq.Edge.makeLine(riser_bend, riser_top), False),
]

tube = cq.Workplane("XY")
for edge, frenet in edges:
    tube = tube.union(sweep(edge, frenet))

show_object(tube)
