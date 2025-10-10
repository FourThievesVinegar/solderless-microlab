import cadquery as cq

# Parameters for the Mason jar with a realistic shape
jar_diameter_middle = 60.0
jar_diameter_bottom = 55.0 
jar_height = 81.0  # mm, total height
jar_thread_height = 71.0
jar_bottom_height = 5.0
jar_wall_thickness = 1.5  # mm
lid_thread_diameter = 64.0  # mm, outer thread diameter
lid_thread_height = 10.0  # mm

# ----------------------------
# 1. Create Outer Jar Shape
# ----------------------------
outer_jar_profile = (
    cq.Workplane("XZ")
    .moveTo(jar_diameter_bottom / 2, 0)  # Start at the base
    .spline(
        listOfXYTuple=[
            (jar_diameter_bottom / 2, 0), 
            (jar_diameter_middle / 2, jar_bottom_height)
        ], 
        tangents=[(0.5, 0.5), (0, 1)]
    )
    .lineTo(jar_diameter_middle / 2, jar_height)
    .lineTo(0, jar_height)  # Close the top
    .lineTo(0, 0)  # Close back to base
    .close()  # Ensure the profile is closed
    .revolve()  # Revolve around the Z-axis
)

# ----------------------------
# 2. Create Inner Jar Shape (for hollowing)
# ----------------------------
inner_jar_profile = (
    cq.Workplane("XZ")
    .moveTo(jar_diameter_bottom / 2 - jar_wall_thickness, jar_wall_thickness)
    .spline(
        listOfXYTuple=[
            (jar_diameter_bottom / 2 - jar_wall_thickness, jar_wall_thickness), 
            (jar_diameter_middle / 2 - jar_wall_thickness, jar_bottom_height)
        ], 
        tangents=[(0.5, 0.5), (0, 1)]
    )
    .lineTo(jar_diameter_middle / 2 - jar_wall_thickness, jar_height)
    .lineTo(0, jar_height)  # Close the top
    .lineTo(0, 0)  # Close back to base
    .close()  # Ensure the profile is closed
    .revolve()  # Revolve around the Z-axis
 )

# ----------------------------
# 3. Subtract Inner Profile from Outer Profile
# ----------------------------
mason_jar = outer_jar_profile.cut(inner_jar_profile)

# TODO: add thread maybe later (standard: 86-400 or 89-400)

show_object(mason_jar)