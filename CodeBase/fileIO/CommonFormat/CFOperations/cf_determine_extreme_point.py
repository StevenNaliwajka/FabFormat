from CodeBase.fileIO.CommonFormat.CFOperations.GeneralMath.calculate_distance_p2p import calculate_distance


def cf_determine_extreme_point(list_of_cf, check_pt, type_code):
    # Given a list of CF and a point.
    # What point in the total list of CF is the furthest or closest away from the chosen point.

    # adding logic to curve calculation could spead things up so I dont have to brute force everything..... TBD

    # Mutable list to save from passing around

    # Extreme POINT LIST ID
    # [0] -  ExtremeX
    # [1] -  ExtremeY
    # [2] -  Current_Distance
    # [3] -  Starting_X
    # [4] -  Starting_Y
    extreme_points_list = [check_pt, 0, check_pt]

    # TYPE CODE INFORMATION
    # 0 - CLOSEST
    # 1 - FURTHEST

    if type_code == 1:
        for cf in list_of_cf:
            extreme_points_list = cf.get_extreme_points()
            for point in extreme_points_list:
                _is_furthest(point, extreme_points_list)

    elif type_code == 0:
        for cf in list_of_cf:
            extreme_points_list = cf.get_extreme_points()
            for point in extreme_points_list:
                _is_closest(point, extreme_points_list)

    # Once iterated through all. Return the furthest.
    return extreme_points_list[0], extreme_points_list[1]


def _is_furthest(check_pt, furthest_point_list):
    # Checks if the check_X and check_Y are further away

    # get distance between Start cords and check cords
    new_distance = calculate_distance(check_pt, (furthest_point_list[3], furthest_point_list[4]))
    if new_distance > furthest_point_list[2]:
        furthest_point_list[2] = new_distance
        furthest_point_list[0] = check_pt[0]
        furthest_point_list[1] = check_pt[1]


def _is_closest(check_pt, furthest_point_list):
    # Checks if the check_X and check_Y are further away

    # get distance between Start cords and check cords
    new_distance = calculate_distance(check_pt, (furthest_point_list[3], furthest_point_list[4]))
    if new_distance < furthest_point_list[2]:
        furthest_point_list[2] = new_distance
        furthest_point_list[0] = check_pt[0]
        furthest_point_list[1] = check_pt[1]
