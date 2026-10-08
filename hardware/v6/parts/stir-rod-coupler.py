import cadquery as cq

if "show_object" not in globals():
    def show_object(*args, **kwargs):
        pass

coupler_diameter = 8.0
coupler_length = 20.0
motor_bore_diameter = 3.0
rod_bore_diameter = 6.0
set_screw_diameter = 2.5

coupler = (
    cq.Workplane("XY")
    .circle(coupler_diameter / 2)
    .extrude(coupler_length)
    .translate((0, 0, -coupler_length / 2))
)

motor_bore = (
    cq.Workplane("XY")
    .circle(motor_bore_diameter / 2)
    .extrude(coupler_length / 2 + 0.2)
)

rod_bore = (
    cq.Workplane("XY")
    .circle(rod_bore_diameter / 2)
    .extrude(coupler_length / 2 + 0.2)
    .translate((0, 0, -coupler_length / 2 - 0.2))
)

set_screw_hole = (
    cq.Workplane("XZ")
    .center(0, -coupler_length / 4)
    .circle(set_screw_diameter / 2)
    .extrude(coupler_diameter + 0.2)
    .translate((0, -coupler_diameter / 2 - 0.1, 0))
)

coupler = coupler.cut(motor_bore).cut(rod_bore).cut(set_screw_hole)

show_object(coupler)
