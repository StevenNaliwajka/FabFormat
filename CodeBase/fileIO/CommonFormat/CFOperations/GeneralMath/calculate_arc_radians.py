import math


def calculate_arc_radians(center, end):
    """
    Calculate the radians of an arc given the center point and the end point.

    :param center: Tuple (x_center, y_center)
    :param end: Tuple (x_end, y_end)
    :return: Radians (float)
    """
    x_center, y_center = center
    x_end, y_end = end

    # Calculate radians using atan2
    radians = math.atan2(y_end - y_center, x_end - x_center)
    return radians