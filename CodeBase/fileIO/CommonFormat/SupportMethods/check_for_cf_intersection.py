def check_for_cf_intersection(list_of_cf, new_cf, pos_in_list):
    # Checks for Common Form intersections between a new_instruction and an existing list of instructions
    # Allows to start at a certain point by returning pos_in_list
    # When intersection is found, handle the intersection, return the updated list

    # When handling intersections, primary goal is for preserving conductivity so an order of
    # Circle > arc > polygon > linear
    # is followed.

    for existing_cf in list_of_cf:
        # FOR EVERY CF run a switcher looking for both conditions.
        # Maybe be smart and do some cool math shit where the two values added together are a unique value
        # That unique value will allow for only two switchers. One to determine the input names
        # One to choose the acceptible processing method
        if existing_cf.type ==
    return None

def circle_circle_intersection
    pass
def circle_arc_intersection
    pass

def circle_polygon_intersection
    pass

def circle_linear_intersection
    pass

def arc_arc_intersection
    pass

def arc_polygon_intersection
    pass

def arc_linear_intersection
    pass

def polygon_polygon_intersection
    pass

def polygon_linear_intersection
    pass

def linear_linear_intersection
    pass