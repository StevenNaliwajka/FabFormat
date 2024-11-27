def fsa_fsa_intersection(fsa1, fsa2):
    def point_distance(pt1, pt2):
        """Calculate the Euclidean distance between two points."""
        return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5

    def is_point_within_arc(pt, arc):
        """Check if a point is within the angular range of an arc."""
        from math import atan2, degrees

        angle_pt = degrees(atan2(pt[1] - arc.center_pt[1], pt[0] - arc.center_pt[0]))
        angle_start = degrees(atan2(arc.start_pt[1] - arc.center_pt[1], arc.start_pt[0] - arc.center_pt[0]))
        angle_end = degrees(atan2(arc.end_pt[1] - arc.center_pt[1], arc.end_pt[0] - arc.center_pt[0]))

        # Normalize angles to [0, 360)
        angle_pt = angle_pt % 360
        angle_start = angle_start % 360
        angle_end = angle_end % 360

        if angle_start <= angle_end:
            return angle_start <= angle_pt <= angle_end
        else:
            return angle_pt >= angle_start or angle_pt <= angle_end

    def circle_intersection_points(center1, r1, center2, r2):
        """Find intersection points of two circles."""
        from math import sqrt

        d = point_distance(center1, center2)

        # No solution if circles are too far apart or one is contained within the other
        if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
            return None

        # Find a and h
        a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
        h = sqrt(r1 ** 2 - a ** 2)

        # Find P2
        x2 = center1[0] + a * (center2[0] - center1[0]) / d
        y2 = center1[1] + a * (center2[1] - center1[1]) / d

        # Find intersection points P3
        x3_1 = x2 + h * (center2[1] - center1[1]) / d
        y3_1 = y2 - h * (center2[0] - center1[0]) / d

        x3_2 = x2 - h * (center2[1] - center1[1]) / d
        y3_2 = y2 + h * (center2[0] - center1[0]) / d

        return (x3_1, y3_1), (x3_2, y3_2)

    # Check intersections between the outer circles of the arcs
    outer_intersections = circle_intersection_points(
        fsa1.center_pt, fsa1.edge_radius, fsa2.center_pt, fsa2.edge_radius
    )

    if outer_intersections:
        outer_left_pt = None
        outer_right_pt = None
        overlap_flag = 0

        for pt in outer_intersections:
            if is_point_within_arc(pt, fsa1) and is_point_within_arc(pt, fsa2):
                if outer_left_pt is None:
                    outer_left_pt = pt
                else:
                    outer_right_pt = pt
                    break

        if outer_left_pt and outer_right_pt:
            overlap_flag = 1

        # Check intersections for the inner circles if they exist
        if fsa1.inner_radius and fsa2.inner_radius:
            inner_intersections = circle_intersection_points(
                fsa1.center_pt, fsa1.inner_radius, fsa2.center_pt, fsa2.inner_radius
            )

            inner_left_pt = None
            inner_right_pt = None

            if inner_intersections:
                for pt in inner_intersections:
                    if is_point_within_arc(pt, fsa1) and is_point_within_arc(pt, fsa2):
                        if inner_left_pt is None:
                            inner_left_pt = pt
                        else:
                            inner_right_pt = pt
                            break

                return fsa1.id, outer_left_pt, outer_right_pt, overlap_flag, inner_left_pt, inner_right_pt

        return fsa1.id, outer_left_pt, outer_right_pt, overlap_flag, None, None

    return None
