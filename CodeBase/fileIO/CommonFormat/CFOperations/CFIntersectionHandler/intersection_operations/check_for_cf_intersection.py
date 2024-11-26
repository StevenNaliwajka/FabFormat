from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.intersection_operations.bounding_box_check import \
    bounding_box_check
from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.intersection_operations.test_intersection import *
# Each common form is given a prime number
common_form_switcher = {
    # Shapes
    "cir": 2,  # Circle
    "fsa": 3,  # Filled_sym_arc
    # Primitives
    "lin": 5,  # Linear_prim
    "pcs": 7,  # Parametric_cub_spline_prim
    "sap": 11, # symm_arc_prim
}

# CF * CF = unique number.
intersection_method_switcher = {
    3: cir_cir_intersection,
    6: cir_fsa_intersection,
    10: cir_lin_intersection,
    14: cir_pcs_intersection,
    22: cir_sap_intersection,
    9: fsa_fsa_intersection,
    15: fsa_lin_intersection,
    21: fsa_pcs_intersection,
    33: fsa_sap_intersection,
    25: lin_lin_intersection,
    35: lin_pcs_intersection,
    55: lin_sap_intersection,
    49: pcs_pcs_intersection,
    77: pcs_sap_intersection,
    121: sap_sap_intersection,

}
def check_for_cf_intersection(old_cf, new_cf):
    # Checks for Common Form intersections between a new_instruction and an existing instruction
    # Gets unique prime CF value
    new_cf_prime_value = common_form_switcher.get(new_cf.type)
    old_cf_prime_value = common_form_switcher.get(old_cf.type)

    bounding_box_1 = old_cf.get_bounding_box()
    bounding_box_2 = new_cf.get_bounding_box()

    if bounding_box_check(bounding_box_1, bounding_box_2):
        resultant = new_cf_prime_value*old_cf_prime_value
        result_method = intersection_method_switcher.get(resultant)
        return result_method(old_cf, new_cf)
    else:
        return True

def check_for_cf_intersection_in_list(cf_list, new_cf):
    # Calls check for cf intersection and returns all of the indexes and methods where the new CF intersects.
    intersection_list = []
    for old_cf in cf_list:
        new_intersection = check_for_cf_intersection(old_cf, new_cf)
        if new_intersection:
            intersection_list.append(new_intersection)
    return intersection_list
