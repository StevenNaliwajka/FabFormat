from CodeBase.fileIO.CommonFormat.CFIntersectionHandler.support.test_intersection import *


def check_for_cf_intersection(list_of_cf, new_cf, pos_in_list):
    # Checks for Common Form intersections between a new_instruction and an existing list of instructions
    # Allows to start at a certain point by returning pos_in_list
    # When intersection is found, handle the intersection, return the updated list

    # When handling intersections, primary goal is for preserving conductivity so an order of
    # Circle > arc > polygon > linear
    # is followed.

    #### MODIFY SUBTRACTIVE TRACE TO JUST CREATE A CIRCLE AND MAKE IT 'SUBTRACTIVE'

    # Each common form is given a prime number
    common_form_switcher = {
        "c": 2,  # Circle
        "a": 3,  # Arc
        "p": 5,  # Polygon
        "l": 7,  # Line
    }

    # CF * CF = unique number.
    intersection_method_switcher = {
        4: circle_circle_intersection,
        6: circle_arc_intersection,
        10: circle_polygon_intersection,
        14: circle_linear_intersection,
        9: arc_arc_intersection,
        15: arc_polygon_intersection,
        21: arc_linear_intersection,
        25: polygon_polygon_intersection,
        35: polygon_linear_intersection,
        49: linear_linear_intersection
    }

    # Gets unique prime CF value
    new_cf_prime = common_form_switcher.get(new_cf.type)
    for index, existing_cf in enumerate(list_of_cf[pos_in_list:], pos_in_list):
        # FOR EVERY CF run a switcher looking for both conditions.
        # Cool math shit with 2 prime numbers to get unique values. :)

        # Gets unique prime CF value
        existing_cf_prime = common_form_switcher.get(existing_cf.type)
        # Gets unique intersection switcher
        intersection_method_id = new_cf_prime * existing_cf_prime
        # Runs the intersection method, returns a new corrected CF list if there was an intersection
        old_cf = existing_cf
        result_method = intersection_method_switcher.get(intersection_method_id)
        result = result_method(old_cf, new_cf)

        if result is not None:
            # Remove old CF value.
            list_of_cf.pop(index)
            list_of_cf.extend(result)
            ## DECIDE HOW TO HANDLE WHETHER TO REPLCE OLD_CF OR NEW_CF OR BOTH.
            # Recursive. Runs till all intersections are handled.
            check_for_cf_intersection(result, new_cf, index)

    return None
