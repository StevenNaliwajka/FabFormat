import math


def cir_cir_intersection(cir1, cir2):
    # Extract attributes for clarity
    center1, radius1, inner_radius1 = cir1.center_pt, cir1.radius, getattr(cir1, "inner_radius", 0)
    center2, radius2, inner_radius2 = cir2.center_pt, cir2.radius, getattr(cir2, "inner_radius", 0)

    def distance(pt1, pt2):
        return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    # Calculate the distance between the centers
    d = distance(center1, center2)

    # Check for outer radius overlap
    outer_overlap_flag = 0
    outer_left_pt = None
    outer_right_pt = None

    if d < radius1 + radius2:  # Overlap
        outer_overlap_flag = 1
        if d == abs(radius1 - radius2):  # Circles touch externally or one is inside the other
            point = (
                center1[0] + (radius2 / d) * (center2[0] - center1[0]),
                center1[1] + (radius2 / d) * (center2[1] - center1[1])
            )
            outer_left_pt = outer_right_pt = point
        else:  # General case of two intersection points
            a = (radius1 ** 2 - radius2 ** 2 + d ** 2) / (2 * d)
            h = math.sqrt(radius1 ** 2 - a ** 2)
            mid_x = center1[0] + a * (center2[0] - center1[0]) / d
            mid_y = center1[1] + a * (center2[1] - center1[1]) / d
            x_offset = h * (center2[1] - center1[1]) / d
            y_offset = h * (center2[0] - center1[0]) / d
            outer_left_pt = (mid_x - x_offset, mid_y + y_offset)
            outer_right_pt = (mid_x + x_offset, mid_y - y_offset)

    # Check for inner radius overlap
    inner_overlap_flag = 0
    inner_left_pt = None
    inner_right_pt = None

    if inner_radius1 > 0 and inner_radius2 > 0:
        if d < inner_radius1 + inner_radius2:  # Overlap
            inner_overlap_flag = 1
            if d == abs(inner_radius1 - inner_radius2):  # Circles touch internally
                point = (
                    center1[0] + (inner_radius2 / d) * (center2[0] - center1[0]),
                    center1[1] + (inner_radius2 / d) * (center2[1] - center1[1])
                )
                inner_left_pt = inner_right_pt = point
            else:  # General case of two intersection points
                a = (inner_radius1 ** 2 - inner_radius2 ** 2 + d ** 2) / (2 * d)
                h = math.sqrt(inner_radius1 ** 2 - a ** 2)
                mid_x = center1[0] + a * (center2[0] - center1[0]) / d
                mid_y = center1[1] + a * (center2[1] - center1[1]) / d
                x_offset = h * (center2[1] - center1[1]) / d
                y_offset = h * (center2[0] - center1[0]) / d
                inner_left_pt = (mid_x - x_offset, mid_y + y_offset)
                inner_right_pt = (mid_x + x_offset, mid_y - y_offset)

    if not outer_left_pt and not inner_left_pt:  # No overlap
        return None

    return (
        cir1.id,
        outer_left_pt, outer_right_pt, outer_overlap_flag,
        inner_left_pt, inner_right_pt
    )
