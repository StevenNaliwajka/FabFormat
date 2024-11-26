import math


def cir_fsa_intersection(cir1, lin1):
    def line_circle_intersections(circle_center, radius, start_pt, end_pt):
        """Find intersections of a line segment and a circle."""
        cx, cy = circle_center
        x1, y1 = start_pt
        x2, y2 = end_pt

        dx = x2 - x1
        dy = y2 - y1

        a = dx ** 2 + dy ** 2
        b = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
        c = (x1 - cx) ** 2 + (y1 - cy) ** 2 - radius ** 2

        det = b ** 2 - 4 * a * c
        if det < 0:
            return None  # No intersection
        elif det == 0:
            t = -b / (2 * a)
            if 0 <= t <= 1:
                return [(x1 + t * dx, y1 + t * dy)]  # Tangent point
            else:
                return None
        else:
            t1 = (-b - math.sqrt(det)) / (2 * a)
            t2 = (-b + math.sqrt(det)) / (2 * a)
            points = []
            if 0 <= t1 <= 1:
                points.append((x1 + t1 * dx, y1 + t1 * dy))
            if 0 <= t2 <= 1:
                points.append((x1 + t2 * dx, y1 + t2 * dy))
            return points

    outer_intersections = line_circle_intersections(cir1.center_pt, cir1.radius, lin1.start_pt, lin1.end_pt)
    inner_intersections = line_circle_intersections(cir1.center_pt, cir1.inner_radius, lin1.start_pt,
                                                    lin1.end_pt) if hasattr(cir1, "inner_radius") else None

    # Combine the two sets of intersection points
    intersection_points = []
    '''
    if outer_intersections:
        intersection_points.extend(outer_intersections)
    if inner_intersections:
        intersection_points.extend(inner_intersections)
    '''
    if not outer_intersections or inner_intersections:
        return None  # No intersection

    # Sort points clockwise relative to the center

    outer_intersections = sorted(outer_intersections,
                                 key=lambda pt: math.atan2(pt[1] - cir1.center_pt[1], pt[0] - cir1.center_pt[0]))
    inner_intersections = sorted(inner_intersections,
                                 key=lambda pt: math.atan2(pt[1] - cir1.center_pt[1], pt[0] - cir1.center_pt[0]))

    outer_left_pt = outer_intersections[0]
    outer_right_pt = outer_intersections[-1]
    inner_left_pt = inner_intersections[0]
    inner_right_pt = inner_intersections[-1]

    # Determine if it bounds or overlaps
    if len(intersection_points) == 1:
        overlap_flag = 0  # Bounding but not overlapping
    else:
        overlap_flag = 1  # Overlapping

    return cir1.id, outer_left_pt, outer_right_pt, overlap_flag, inner_left_pt, inner_right_pt
