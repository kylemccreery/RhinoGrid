import Rhino
import scriptcontext
import System.Guid
import rhinoscriptsyntax as rs


def rounded_rectangle(x_coord, y_coord, z_coord, length, width, radius):
    rs.Command("_Rectangle _Rounded " + str(x_coord) + "," + str(y_coord) + "," + str(z_coord) + " " + str(length) + " " + str(width) + " " + str(radius), False)
    return rs.LastCreatedObjects()


def surface_from_parallels(first_curve, second_curve):
    exploded_first = rs.ExplodeCurves(first_curve)
    exploded_second = rs.ExplodeCurves(second_curve)
    
    corners_first = []
    horiz_first = []
    vert_first = []
    for each_curve in exploded_first:
        if rs.coercecurve(each_curve).IsArc():
            corners_first += [each_curve]
        elif rs.coercecurve(each_curve).IsLinear():
            if rs.CurveEndPoint(each_curve).X == rs.CurveStartPoint(each_curve).X:
                vert_first += [each_curve]
            elif rs.CurveEndPoint(each_curve).Y == rs.CurveStartPoint(each_curve).Y:
                horiz_first += [each_curve]
                
    corners_second = []
    horiz_second = []
    vert_second = []
    for each_curve in exploded_second:
        if rs.coercecurve(each_curve).IsArc():
            corners_second += [each_curve]
        elif rs.coercecurve(each_curve).IsLinear():
            if rs.CurveEndPoint(each_curve).X == rs.CurveStartPoint(each_curve).X:
                vert_second += [each_curve]
            elif rs.CurveEndPoint(each_curve).Y == rs.CurveStartPoint(each_curve).Y:
                horiz_second += [each_curve]
    
    corners_first.sort(key=lambda c: (round(rs.CurveMidPoint(c).X, 3), round(rs.CurveMidPoint(c).Y, 3)))
    corners_second.sort(key=lambda c: (round(rs.CurveMidPoint(c).X, 3), round(rs.CurveMidPoint(c).Y, 3)))
    
    horiz_first.sort(key=lambda c: (round(rs.CurveMidPoint(c).X, 3), round(rs.CurveMidPoint(c).Y, 3)))
    horiz_second.sort(key=lambda c: (round(rs.CurveMidPoint(c).X, 3), round(rs.CurveMidPoint(c).Y, 3)))

    vert_first.sort(key=lambda c: (round(rs.CurveMidPoint(c).X, 3), round(rs.CurveMidPoint(c).Y, 3)))
    vert_second.sort(key=lambda c: (round(rs.CurveMidPoint(c).X, 3), round(rs.CurveMidPoint(c).Y, 3)))
    rail_lines = []
    sweeps = []
    
    for each_index in range(0,len(corners_first)):
        if round(rs.CurveStartPoint(corners_first[each_index]).X, 3) == round(rs.CurveStartPoint(corners_second[each_index]).X, 3):
            shape_line = rs.AddLine(rs.CurveStartPoint(corners_first[each_index]), rs.CurveStartPoint(corners_second[each_index]))
        elif round(rs.CurveStartPoint(corners_first[each_index]).X, 3) == round(rs.CurveEndPoint(corners_second[each_index]).X, 3):
            shape_line = rs.AddLine(rs.CurveStartPoint(corners_first[each_index]), rs.CurveEndPoint(corners_second[each_index]))
        elif round(rs.CurveEndPoint(corners_first[each_index]).X, 3) == round(rs.CurveStartPoint(corners_second[each_index]).X, 3):
            shape_line = rs.AddLine(rs.CurveEndPoint(corners_first[each_index]), rs.CurveStartPoint(corners_second[each_index]))
        elif round(rs.CurveEndPoint(corners_first[each_index]).X, 3) == round(rs.CurveEndPoint(corners_second[each_index]).X, 3):
            shape_line = rs.AddLine(rs.CurveEndPoint(corners_first[each_index]), rs.CurveEndPoint(corners_second[each_index]))
        else:
            break

        rails = [str(rs.coerceguid(corners_first[each_index])), str(rs.coerceguid(corners_second[each_index]))]
        sweeps += [rs.AddSweep2(rails, [shape_line])]
        rail_lines += [shape_line]

    for each_index in range(0,len(horiz_first)):
        if round(rs.CurveStartPoint(horiz_first[each_index]).X, 3) == round(rs.CurveStartPoint(horiz_second[each_index]).X, 3):
            shape_line = rs.AddLine(rs.CurveStartPoint(horiz_first[each_index]), rs.CurveStartPoint(horiz_second[each_index]))
        elif round(rs.CurveStartPoint(horiz_first[each_index]).X, 3) == round(rs.CurveEndPoint(horiz_second[each_index]).X, 3):
            shape_line = rs.AddLine(rs.CurveStartPoint(horiz_first[each_index]), rs.CurveEndPoint(horiz_second[each_index]))
        elif round(rs.CurveEndPoint(horiz_first[each_index]).X, 3) == round(rs.CurveStartPoint(horiz_second[each_index]).X, 3):
            shape_line = rs.AddLine(rs.CurveEndPoint(horiz_first[each_index]), rs.CurveStartPoint(horiz_second[each_index]))
        elif round(rs.CurveEndPoint(horiz_first[each_index]).X, 3) == round(rs.CurveEndPoint(horiz_second[each_index]).X, 3):
            shape_line = rs.AddLine(rs.CurveEndPoint(horiz_first[each_index]), rs.CurveEndPoint(horiz_second[each_index]))
        else:
            break

        rails = [str(rs.coerceguid(horiz_first[each_index])), str(rs.coerceguid(horiz_second[each_index]))]
        sweeps += [rs.AddSweep2(rails, [shape_line])]
        rail_lines += [shape_line]

    for each_index in range(0,len(vert_first)):
        if round(rs.CurveStartPoint(vert_first[each_index]).Y, 3) == round(rs.CurveStartPoint(vert_second[each_index]).Y, 3):
            shape_line = rs.AddLine(rs.CurveStartPoint(vert_first[each_index]), rs.CurveStartPoint(vert_second[each_index]))
        elif round(rs.CurveStartPoint(vert_first[each_index]).Y, 3) == round(rs.CurveEndPoint(vert_second[each_index]).Y, 3):
            shape_line = rs.AddLine(rs.CurveStartPoint(vert_first[each_index]), rs.CurveEndPoint(vert_second[each_index]))
        elif round(rs.CurveEndPoint(vert_first[each_index]).Y, 3) == round(rs.CurveStartPoint(vert_second[each_index]).Y, 3):
            shape_line = rs.AddLine(rs.CurveEndPoint(vert_first[each_index]), rs.CurveStartPoint(vert_second[each_index]))
        elif round(rs.CurveEndPoint(vert_first[each_index]).Y, 3) == round(rs.CurveEndPoint(vert_second[each_index]).Y, 3):
            shape_line = rs.AddLine(rs.CurveEndPoint(vert_first[each_index]), rs.CurveEndPoint(vert_second[each_index]))
        else:
            break

        rails = [str(rs.coerceguid(vert_first[each_index])), str(rs.coerceguid(vert_second[each_index]))]
        sweeps += [rs.AddSweep2(rails, [shape_line])]
        rail_lines += [shape_line]

    joined_sweep = rs.JoinSurfaces(sweeps, True)
    
    rs.DeleteObjects(rail_lines)
    rs.DeleteObjects(exploded_first)
    rs.DeleteObjects(exploded_second)

    return joined_sweep


def create_top_lip(base_point, length_units, width_units, height_units):
    standard_height = 7
    standard_width = 42
    tolerance_mod = 0.5
    lip_height = 4.4
    inner_offset = 2.6
    middle_offset = 1.9
    outter_radius = 3.75 # stays 3.75 and not bumped up to the normal base plate outter radius of 4 because it is trimmed to match outter walls of bin base shape
    inner_radius = 1.15
    middle_radius = 1.85
    
    lower_chamfer_height = 0.7
    upper_chamfer_height = 2.5
    
    outter_origin = [base_point.X, base_point.Y]
    inner_origin = [base_point.X + inner_offset, base_point.Y + inner_offset]
    middle_origin = [base_point.X + middle_offset, base_point.Y + middle_offset]
    
    height_base = height_units * standard_height
    length_base = length_units * standard_width - tolerance_mod
    width_base = width_units * standard_width - tolerance_mod
    inner_mod = inner_offset * 2
    middle_mod = middle_offset * 2
    
    temp_curves = []        # Deleted later as cleanup
    
    outter_bottom_guid = rounded_rectangle(outter_origin[0], outter_origin[1], height_base, length_base, width_base, outter_radius)
    temp_curves += [outter_bottom_guid]

    outter_top_guid = rounded_rectangle(outter_origin[0], outter_origin[1], height_base + lip_height, length_base, width_base, outter_radius)
    temp_curves += [outter_top_guid]
    
    inner_bottom_guid = rounded_rectangle(inner_origin[0], inner_origin[1], height_base, length_base - inner_mod, width_base - inner_mod, inner_radius)
    temp_curves += [inner_bottom_guid]

    inner_middle_guid = rounded_rectangle(middle_origin[0], middle_origin[1], height_base + lower_chamfer_height, length_base - middle_mod, width_base - middle_mod, middle_radius)
    temp_curves += [inner_middle_guid]

    inner_top_guid = rounded_rectangle(middle_origin[0], middle_origin[1], height_base + upper_chamfer_height, length_base - middle_mod, width_base - middle_mod, middle_radius)
    temp_curves += [inner_top_guid]
    
    to_combine = []
    larger_plane = rs.AddPlanarSrf(outter_bottom_guid)
    smaller_plane = rs.AddPlanarSrf(inner_bottom_guid)
    trimmed_plane = rs.BooleanDifference(larger_plane, smaller_plane)
    to_combine += [trimmed_plane]

    to_combine += [surface_from_parallels(outter_bottom_guid, outter_top_guid)]
    to_combine += [surface_from_parallels(outter_top_guid, inner_top_guid)]
    to_combine += [surface_from_parallels(inner_top_guid, inner_middle_guid)]
    to_combine += [surface_from_parallels(inner_middle_guid, inner_bottom_guid)]
    
    assembled_top_lip = rs.JoinSurfaces(to_combine, True)
    rs.DeleteObjects(temp_curves)
    
    return assembled_top_lip


def create_magnet_cutouts(base_point):
    
    standard_width = 42
    tolerance_mod = 0.5
    
    hole_center_offset = 7.75
    
    magnet_depth = 2.1
    magnet_radius = 3.05
    
    base_width = standard_width - tolerance_mod
    hole_centers = [
        [base_point.X + hole_center_offset, base_point.Y + hole_center_offset, 0],
        [base_point.X + base_width - hole_center_offset, base_point.Y + hole_center_offset, 0],
        [base_point.X + hole_center_offset, base_point.Y + base_width - hole_center_offset, 0],
        [base_point.X + base_width - hole_center_offset, base_point.Y + base_width - hole_center_offset, 0]
    ]

    magnet_holes = [
        rs.AddCylinder(hole_centers[0], magnet_depth, magnet_radius),
        rs.AddCylinder(hole_centers[1], magnet_depth, magnet_radius),
        rs.AddCylinder(hole_centers[2], magnet_depth, magnet_radius),
        rs.AddCylinder(hole_centers[3], magnet_depth, magnet_radius)
    ]
        
    return magnet_holes


def create_screw_cutouts(base_point):
    
    standard_width = 42
    tolerance_mod = 0.5
    
    hole_center_offset = 7.75
    
    screw_depth = 4.75
    screw_radius = 1.55
    
    base_width = standard_width - tolerance_mod
    hole_centers = [
        [base_point.X + hole_center_offset, base_point.Y + hole_center_offset, 0],
        [base_point.X + base_width - hole_center_offset, base_point.Y + hole_center_offset, 0],
        [base_point.X + hole_center_offset, base_point.Y + base_width - hole_center_offset, 0],
        [base_point.X + base_width - hole_center_offset, base_point.Y + base_width - hole_center_offset, 0]
    ]

    screw_holes = [
        rs.AddCylinder(hole_centers[0], screw_depth, screw_radius),
        rs.AddCylinder(hole_centers[1], screw_depth, screw_radius),
        rs.AddCylinder(hole_centers[2], screw_depth, screw_radius),
        rs.AddCylinder(hole_centers[3], screw_depth, screw_radius)
    ]

    return screw_holes


def add_top_spacer_to_base(base_point, length_units, width_units):
    standard_height = 7
    standard_width = 42
    tolerance_mod = 0.5
    outter_radius = 3.75
    cap_z_offset = 4.75
    
    length_base = length_units * standard_width - tolerance_mod
    width_base = width_units * standard_width - tolerance_mod
    
    outter_origin = [base_point.X, base_point.Y]
    
    temp_curves = []
    

    lower_curve_guid = rounded_rectangle(outter_origin[0], outter_origin[1], cap_z_offset, length_base, width_base, outter_radius)
    temp_curves += [lower_curve_guid]
    
    upper_curve_guid = rounded_rectangle(outter_origin[0], outter_origin[1], standard_height, length_base, width_base, outter_radius)
    temp_curves += [upper_curve_guid]

    topper_parts = [
        rs.AddPlanarSrf(lower_curve_guid),
        rs.AddPlanarSrf(upper_curve_guid),
        surface_from_parallels(lower_curve_guid, upper_curve_guid)
    ]
    assembled_topper = rs.JoinSurfaces(topper_parts, True)

    rs.DeleteObjects(temp_curves)

    return assembled_topper


def create_bottom_unit_shape(base_point, add_magnets=True, add_screws=True):
    standard_width = 42
    tolerance_mod = 0.5

    inner_offset = 2.95
    middle_offset = 2.15
    
    inner_radius = 0.8
    middle_radius = 1.6
    outter_radius = 3.75
    
    lower_chamfer_height = 0.8
    upper_chamfer_height = 2.6
    top_height = 4.75
    
    base_width = standard_width - tolerance_mod
    inner_mod = inner_offset * 2
    middle_mod = middle_offset * 2

    inner_origin = [base_point.X + inner_offset, base_point.Y + inner_offset]
    middle_origin = [base_point.X + middle_offset, base_point.Y + middle_offset]
    outter_origin = [base_point.X, base_point.Y]
    
    temp_curves = []
    
    top_guid = rounded_rectangle(outter_origin[0], outter_origin[1], top_height, base_width, base_width, outter_radius)
    temp_curves += [top_guid]
    
    upper_middle_guid = rounded_rectangle(middle_origin[0], middle_origin[1], upper_chamfer_height, base_width - middle_mod, base_width - middle_mod, middle_radius)
    temp_curves += [upper_middle_guid]
    
    lower_middle_guid = rounded_rectangle(middle_origin[0], middle_origin[1], lower_chamfer_height, base_width - middle_mod, base_width - middle_mod, middle_radius)
    temp_curves += [lower_middle_guid]
    
    bottom_guid = rounded_rectangle(inner_origin[0], inner_origin[1], 0, base_width - inner_mod, base_width - inner_mod, inner_radius)
    temp_curves += [bottom_guid]

    to_combine = []
    to_combine += [rs.AddPlanarSrf(bottom_guid)] #   Adds plane
    to_combine += [rs.AddPlanarSrf(top_guid)]  #   Adds plane
    to_combine += [surface_from_parallels(bottom_guid, lower_middle_guid)]
    to_combine += [surface_from_parallels(lower_middle_guid, upper_middle_guid)]
    to_combine += [surface_from_parallels(upper_middle_guid, top_guid)]
    assembled_base = rs.JoinSurfaces(to_combine, True)

    magnet_holes = []
    screw_holes = []
    
    if add_magnets:
        magnet_holes = create_magnet_cutouts(base_point)
    
    if add_screws:
        screw_holes = create_screw_cutouts(base_point)
        
    sans_magnets = rs.BooleanDifference(assembled_base, magnet_holes)    # only actually does magnet holes if they were created (default)
    assembled_base = rs.BooleanDifference(sans_magnets, screw_holes) # only actually does screw holes if they were created (default)

    rs.DeleteObjects(temp_curves)
    
    return assembled_base


def create_bin_walls(base_point, length_units, width_units, height_units, taper_top = True, taper_bottom = True, wall_thickness = 1.2):
    standard_height = 7
    standard_width = 42
    tolerance_mod = 0.5
    outter_radius = 3.75
    taper_width = 2.6       # Matches inner lower edge of top stacking lip to create a more printable slope
    
    inner_radius = outter_radius - wall_thickness
    taper_radius = outter_radius - taper_width
    
    length_base = length_units * standard_width - tolerance_mod
    width_base = width_units * standard_width - tolerance_mod
    inner_mod = wall_thickness * 2
    taper_mod = taper_width * 2
    taper_height_mod = taper_width - wall_thickness
    
    outter_origin = [base_point.X, base_point.Y]
    inner_origin = [base_point.X + wall_thickness, base_point.Y + wall_thickness]
    taper_origin = [base_point.X + taper_width, base_point.Y + taper_width]
    
    temp_curves = []
    
    lower_outter_guid = rounded_rectangle(outter_origin[0], outter_origin[1], standard_height, length_base, width_base, outter_radius)
    temp_curves += [lower_outter_guid]
    
    upper_outter_guid = rounded_rectangle(outter_origin[0], outter_origin[1], standard_height * height_units, length_base, width_base, outter_radius)
    temp_curves += [upper_outter_guid]
        
    to_combine = []     # Set here because taper will need to draw before the rest

    if taper_bottom:
        taper_bottom_guid = rounded_rectangle(taper_origin[0], taper_origin[1], standard_height, length_base - taper_mod, width_base - taper_mod, taper_radius)
        temp_curves += [taper_bottom_guid]
        lower_inner_guid = rounded_rectangle(inner_origin[0], inner_origin[1], standard_height + taper_height_mod, length_base - inner_mod, width_base - inner_mod, inner_radius)
        to_combine += [surface_from_parallels(taper_bottom_guid, lower_inner_guid)]
        lower_inner_plane = rs.AddPlanarSrf(taper_bottom_guid)
    else:
        lower_inner_guid = rounded_rectangle(inner_origin[0], inner_origin[1], standard_height, length_base - inner_mod, width_base - inner_mod, inner_radius)
        lower_inner_plane = rs.AddPlanarSrf(lower_inner_guid)

    temp_curves += [lower_inner_guid]

    lower_outter_plane = rs.AddPlanarSrf(lower_outter_guid)
    lower_trimmed_plane = rs.BooleanDifference(lower_outter_plane, lower_inner_plane)
    to_combine += [lower_trimmed_plane]

    if taper_top:
        taper_top_guid = rounded_rectangle(taper_origin[0], taper_origin[1], standard_height * height_units , length_base - taper_mod, width_base - taper_mod, taper_radius)
        temp_curves += [taper_top_guid]
        upper_inner_guid = rounded_rectangle(inner_origin[0], inner_origin[1], standard_height * height_units - taper_height_mod, length_base - inner_mod, width_base - inner_mod, inner_radius)
        to_combine += [surface_from_parallels(taper_top_guid, upper_inner_guid)]
        upper_inner_plane = rs.AddPlanarSrf(taper_top_guid)
    else:
        upper_inner_guid = rounded_rectangle(inner_origin[0], inner_origin[1], standard_height * height_units, length_base - inner_mod, width_base - inner_mod, inner_radius)
        upper_inner_plane = rs.AddPlanarSrf(upper_inner_guid)

    temp_curves += [upper_inner_guid]

    upper_outter_plane = rs.AddPlanarSrf(upper_outter_guid)
    upper_trimmed_plane = rs.BooleanDifference(upper_outter_plane, upper_inner_plane)
    to_combine += [upper_trimmed_plane]
    
    to_combine += [surface_from_parallels(lower_outter_guid, upper_outter_guid)]
    to_combine += [surface_from_parallels(lower_inner_guid, upper_inner_guid)]

    assembled_bin_walls = rs.JoinSurfaces(to_combine, True)

    rs.DeleteObjects(temp_curves)

    return assembled_bin_walls


def build_tiled_base(base_point, length_units, width_units):
    standard_width = 42

    base_segments = []
    for length_unit in range(0,length_units):
        cur_x = base_point.X + length_unit * standard_width
        for width_unit in range(0,width_units):
            cur_y = base_point.Y + width_unit * standard_width
            base_segments += [create_bottom_unit_shape(Rhino.Geometry.Point3d(cur_x, cur_y, 0), True)]
    base_segments += [add_top_spacer_to_base(base_point, length_units, width_units)]
    assembled_base = rs.BooleanUnion(base_segments)
    return assembled_base


def build_full_bin(base_point, length_units, width_units, height_units):

    to_combine = []
    to_combine += [build_tiled_base(base_point, length_units, width_units)]
    to_combine += [create_bin_walls(base_point, length_units, width_units, height_units)]
    to_combine += [create_top_lip(base_point, length_units, width_units, height_units)]
    assembled_bin = rs.BooleanUnion(to_combine)
    
    return assembled_bin
