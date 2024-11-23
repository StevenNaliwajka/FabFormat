import math

from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFPrimitives.cf_parametric_cubic_spline_prim import \
    CFParametricCubicSplinePrim
from CodeBase.fileIO.CommonFormat.CFOperations.GeneralMath.calculate_distance_p2p import calculate_distance


def cf_determine_furthest_point(list_of_cf, point_x, point_y):
    # Given a list of CF and a point.
    # What point in the total list of CF is the furthest away from the chosen point.

    # Mutable list to save from passing around
    furthest_point_list = [point_x, point_y, 0, point_x, point_y]
    # FURTHEST POINT LIST ID
    # [0] -  FurthestX
    # [1] -  FurthestY
    # [2] -  Current_Distance
    # [3] -  Starting_X
    # [4] -  Starting_Y

    for cf in list_of_cf:
        # Composites
        if cf.type == "com":
            _cf_determine_furthest_point_complex_shape(cf, furthest_point_list)
        elif cf.type == "pol":
            _cf_determine_furthest_point_polygon(cf, furthest_point_list)

        #  Primitives
        elif cf.type == "lin":
            _cf_determine_furthest_point_linear_prim(cf, furthest_point_list)
        elif cf.type == "pcs":
            _cf_determine_furthest_point_parametric_cubic_spline_prim(cf, furthest_point_list)
        elif cf.type == "sap":
            _cf_determine_furthest_point_symmetrical_arc_prim(cf, furthest_point_list)

        # Solids
        elif cf.type == "cir":
            _cf_determine_furthest_point_circle(cf, furthest_point_list)
        elif cf.type == "fsa":
            _cf_determine_furthest_point_filled_symmetrical_arc(cf, furthest_point_list)

    # Once iterated through all. Return the furthest.
    return furthest_point_list[0], furthest_point_list[1]


# COMPOSITES
def _cf_determine_furthest_point_complex_shape(cf_complex, furthest_point_list):
    # Just calls primitives
    for cf in cf_complex:
        if cf.type == "lin":
            _cf_determine_furthest_point_linear_prim(cf, furthest_point_list)


def _cf_determine_furthest_point_polygon(cf_polygon, furthest_point_list):
    # Just calls primitives
    for cf in cf_polygon:
        if cf.type == "lin":
            _cf_determine_furthest_point_linear_prim(cf, furthest_point_list)
        elif cf.type == "pcs":
            _cf_determine_furthest_point_parametric_cubic_spline_prim(cf, furthest_point_list)
        elif cf.type == "sap":
            _cf_determine_furthest_point_symmetrical_arc_prim(cf, furthest_point_list)


# PRIMITIVES
def _cf_determine_furthest_point_linear_prim(cf_line, furthest_point_list):
    # By nature of linear, it's either the beginning or the end.
    # No need to calculate fancy stuff.
    _is_further(cf_line.start_y, cf_line.start_y, furthest_point_list)
    _is_further(cf_line.end_x, cf_line.end_y, furthest_point_list)


def _cf_determine_furthest_point_parametric_cubic_spline_prim(cf_para_cub_spline, furthest_point_list):
    # for every point generated
    for t in CFParametricCubicSplinePrim.t_list:
        # get the X,y for the equation
        gotten_x, gotten_y = cf_para_cub_spline.get_point(t)
        # Check further
        _is_further(gotten_x, gotten_y, furthest_point_list)


def _cf_determine_furthest_point_symmetrical_arc_prim(cf_sym_arc_prim, furthest_point_list):
    # the important numbers are the start of curve, end of curve and the max radius point


    # this is only true if the arc radius is shorter or longer than the start+end radius
    if cf_sym_arc_prim.arc_radius != cf_sym_arc_prim.edge_radius:
        _is_further(cf_sym_arc_prim.start_x, cf_sym_arc_prim.start_y, furthest_point_list)
        _is_further(cf_sym_arc_prim.radius_x, cf_sym_arc_prim.radius_y, furthest_point_list)
        _is_further(cf_sym_arc_prim.end_x, cf_sym_arc_prim.end_y, furthest_point_list)

    # if the arc radius is the same as start+end radius then
    else:
        _is_further_circle_segment()


# SOLIDS
def _cf_determine_furthest_point_circle(cf_circle, furthest_point_list):
    _is_further_circle_segment()


def _cf_determine_furthest_point_filled_symmetrical_arc(cf_filled_sym_arc, furthest_point_list):



def _is_further(check_x, check_y, furthest_point_list):
    # Checks if the check_X and check_Y are further away
    # FURTHEST POINT LIST ID
    # [0] -  FurthestX
    # [1] -  FurthestY
    # [2] -  Current_Distance
    # [3] -  Starting_X
    # [4] -  Starting_Y

    # get distance between Start cords and check cords
    new_distance = calculate_distance(check_x, check_y, furthest_point_list[3], furthest_point_list[4])
    if new_distance > furthest_point_list[2]:
        furthest_point_list[0] = check_x
        furthest_point_list[1] = check_y


def _is_further_circle_segment(circle_center, )
    # write method to determine what part of the circle is further..... should handle full circles and partial circles.

