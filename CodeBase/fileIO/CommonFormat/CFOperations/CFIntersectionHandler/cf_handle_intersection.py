def cf_handle_intersection(intersection_flag, intersection_data, common_format):
    # intersection_flag = TRUE: Additive, False: Subtractive

    # Data provided by intersection detection
    # intersection_data is a touple of the following data
    # [cf_1, cf_2, cf1_outer_pt_list, cf1_inner_pt_list, cf2_outer_pt_list, cf2_inner_pt_list, overlap_flag,
    # enveloped_case]
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

    # gets prime numbers
    cf_1_val = common_format.cf_shape_switcher.get(intersection_data[0].type)
    cf_2_val = common_format.cf_shape_switcher.get(intersection_data[1].type)
    cf_multiplied = cf_1_val * cf_2_val

    result_method = None
    # Subtractive
    if intersection_flag is False:
        result_method = common_format.subtractive_handling_switcher.get(cf_multiplied)
    # addtiive
    elif intersection_flag is True:
        result_method = common_format.additive_handling_switcher.get(cf_multiplied)

    return result_method(intersection_data)
