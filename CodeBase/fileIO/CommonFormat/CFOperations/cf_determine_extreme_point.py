from CodeBase.fileIO.CommonFormat.CFOperations.GeneralMath.calculate_distance_p2p import calculate_distance_p2p


def cf_determine_extreme_point(list_of_cf, check_pt, type_code):
    # Given a list of CF and a point.
    # returns 1 extreme point (closest, or furthest)
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
    extreme_index = None
    if type_code == 1:
        for cf in list_of_cf:
            extreme_points_list = cf.get_extreme_points()
            for index, point in enumerate(extreme_points_list):
                if _is_furthest(point, extreme_points_list):
                    extreme_index = point


    elif type_code == 0:
        for cf in list_of_cf:
            extreme_points_list = cf.get_extreme_points()
            for index, point in enumerate(extreme_points_list):
                if _is_closest(point, extreme_points_list):
                    extreme_index = point

    # Once iterated through all. Return the furthest.
    return (extreme_points_list[0], extreme_points_list[1]), extreme_index


def _is_furthest(check_pt, furthest_point_list):
    # Checks if the check_X and check_Y are further away
    # returns true if further

    # get distance between Start cords and check cords
    new_distance = calculate_distance_p2p(check_pt, (furthest_point_list[3], furthest_point_list[4]))
    if new_distance > furthest_point_list[2]:
        furthest_point_list[2] = new_distance
        furthest_point_list[0] = check_pt[0]
        furthest_point_list[1] = check_pt[1]
        return True
    else:
        return False


def _is_closest(check_pt, furthest_point_list):
    # Checks if the check_X and check_Y are further away
    # returns true if closer

    # get distance between Start cords and check cords
    new_distance = calculate_distance_p2p(check_pt, (furthest_point_list[3], furthest_point_list[4]))
    if new_distance < furthest_point_list[2]:
        furthest_point_list[2] = new_distance
        furthest_point_list[0] = check_pt[0]
        furthest_point_list[1] = check_pt[1]
        return True
    else:
        return False
