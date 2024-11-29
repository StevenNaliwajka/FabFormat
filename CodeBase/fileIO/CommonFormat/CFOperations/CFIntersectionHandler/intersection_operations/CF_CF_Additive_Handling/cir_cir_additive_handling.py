from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFComposites.cf_complex_shape import CFComplexShape
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFPrimitives.cf_symmetrical_arc_prim import \
    CFSymmetricalArcPrim
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_circle import CFCircle
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_filled_symmetrical_arc import CFFilledSymmetricalArc
from CodeBase.fileIO.CommonFormat.CFOperations.GeneralMath.calculate_distance_p2p import calculate_distance_p2p
from CodeBase.fileIO.CommonFormat.CFOperations.cf_sym_arc_calculations import find_center_pt_on_sym_arc


def cir_cir_additive_handling(intersection_data):
    # Parses CIR CIR additively, returns resultant shapes. or none if no change.
    # See "CIR_CIR_pt_1.jpg"/"CIR_CIR_pt_2.jpg" for "case" references in documentation folder

    # Intersection_data:
    # [0] cf_1
    # [1] cf_2
    # [2] cf1_outer_pt_list = Intersection pts on outer of cf1
    # [3] cf1_inner_pt_list = Intersection pts on inner of cf1
    # [4] cf2_outer_pt_list = Intersection pts on outer of cf2
    # [5] cf2_inner_pt_list = Intersection pts on inner of cf2
    # [6] overlap_flag = True: Overlapping, handle case
    #                    False: Touching, do nothing
    # [7] enveloped_case = 1: If cf1 is entirely enveloped by cf2, remove it
    #                      2: if cf2 is entirely enveloped by cf1, remove it
    #                      0: default, nothing

    # Overlap_case already handled in "cf_handle_intersection": Ignore

    # Enveloped_case already handled in "cf_handle_intersection": Ignore
    # case 3

    parsed_cf_list = []
    cir1 = intersection_data[0]
    cir2 = intersection_data[1]
    cir1_outer = intersection_data[2]
    cir1_inner = intersection_data[3]
    cir2_outer = intersection_data[4]
    cir2_inner = intersection_data[5]


    if cir1_outer and cir2_outer:
        if cir1_inner and cir2_inner:
            # case 7
            _case_7(parsed_cf_list, cir1, cir2, cir1_outer, cir1_inner, cir2_outer, cir2_inner)

        elif cir1_inner or cir2_inner:
            # case 2
            # case 6
        else:
            # case 1
            # case 4
            # case 5

    elif cir1_outer or cir2_outer:
        if cir1_inner and cir2_inner:
            #
        elif cir1_inner or cir2_inner:
            #
        else:
            #

    else:



    return parsed_cf_list

def _case_7(parsed_cf_list, cir1, cir2, cir1_outer, cir1_inner, cir2_outer, cir2_inner):
    if cir1.radius > cir2.radius:
        bigger = cir1
        bigger_outer = cir1_outer
        bigger_inner = cir1_inner
        smaller_outer = cir2_outer
        smaller_inner = cir2_inner
    else:
        bigger = cir2
        bigger_outer = cir2_outer
        bigger_inner = cir2_inner
        smaller_outer = cir1_outer
        smaller_inner = cir1_inner
    parsed_cf_list.append(bigger)

    com1_list = []
    # building 2fsa com
    com1_list.append(_create_sap(bigger, bigger_inner[1], bigger_inner[0]))
    com1_list.append(_create_sap(bigger, bigger_inner[0], bigger_inner[1]))
    parsed_cf_list.append(_create_com(com1_list))

    # building 4 sap com
    com2_list = []
    com2_list.append(_create_sap(bigger, smaller_outer[-1], smaller_outer[0]))
    com2_list.append(_create_sap(bigger_outer[0], smaller_inner))
    com2_list.append(_create_sap(bigger, smaller_inner([-1]),smaller_inner[0]))



def _create_sap(bigger, start_pt, end_pt):
    center_1 = find_center_pt_on_sym_arc(start_pt, end_pt)
    arc_radius = calculate_distance_p2p(start_pt, center_1)
    return CFSymmetricalArcPrim(bigger.unit, center_1, start_pt, end_pt, arc_radius)
def _create_com(list_of_prim):
    return CFComplexShape(list_of_prim[0].unit, list_of_prim)