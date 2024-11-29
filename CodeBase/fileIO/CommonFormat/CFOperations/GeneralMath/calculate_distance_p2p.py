import math


def calculate_distance_p2p(pt_one, pt_two):
    return math.sqrt((pt_two[0] - pt_one[0]) ** 2 + (pt_two[1] - pt_one[1]) ** 2)
