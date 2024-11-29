from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.intersection_operations.CF_CF_Intersection_test import \
    cir_cir_intersection, cir_fsa_intersection, cir_lin_intersection, cir_pcs_intersection, cir_sap_intersection, \
    fsa_fsa_intersection, fsa_lin_intersection, fsa_pcs_intersection, fsa_sap_intersection, lin_lin_intersection, \
    lin_sap_intersection, lin_pcs_intersection, pcs_pcs_intersection, pcs_sap_intersection, sap_sap_intersection
from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.intersection_operations.bounding_box_check import \
    bounding_box_check

def check_for_cf_intersection(old_cf_list, new_cf, common_format):
    # NEEDS TO BE UPDATED TO REQUIRED FORMAT FROM HANDLE_INTERSECTIONS

    # Checks for Common Form intersections between a new_instruction and an existing instruction
    # Gets unique prime CF value

    # if intersection occurs, return:
    # ---------------
    # (cf.id, pt_one, pt_two, 1/0)
    # -------------
    # CF.ID - ID OF THE OLD_CF
    # Points are sored with clockwise rotation in mind.
    # pt_one - "left" side intersection
    # pt_two - "right" side intersection
    # 1/0: 1 means it overlaps, 0 means it just touches.

    # if old CF is Composite
    intersection_list = []
    if isinstance(old_cf_list, list):
        for cf in old_cf_list:
            _check_with_formating(cf, new_cf, intersection_list, common_format)
    else:
        _check_with_formating(old_cf_list, new_cf, intersection_list, common_format)

    return intersection_list


def _check_with_formating(old_cf, new_cf, intersection_list, common_format):
    composite_cf = {"com", "pol"}
    if old_cf.type in composite_cf:
        for cf in old_cf:
            intersection = _check_for_cf_intersection(cf, new_cf, common_format)
            if intersection:
                intersection_list.append(intersection)
    elif new_cf.type in composite_cf:
        for cf in new_cf:
            intersection = _check_for_cf_intersection(old_cf, cf, common_format)
            if intersection:
                intersection_list.append(intersection)
    else:
        intersection = _check_for_cf_intersection(old_cf, new_cf, common_format)
        if intersection:
            intersection_list.append(intersection)
    return intersection_list


def _check_for_cf_intersection(old_cf, new_cf, common_format):
    new_cf_prime_value = common_format.cf_shape_switcher.get(new_cf.type)
    old_cf_prime_value = common_format.cf_shape_switcher.get(old_cf.type)

    bounding_box_1 = old_cf.get_bounding_box()
    bounding_box_2 = new_cf.get_bounding_box()

    if bounding_box_check(bounding_box_1, bounding_box_2):
        resultant = new_cf_prime_value * old_cf_prime_value
        result_method = common_format.intersection_method_switcher.get(resultant)
        return result_method(old_cf, new_cf)
    else:
        return False
