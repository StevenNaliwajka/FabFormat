def lin_pcs_intersection(lin1, pcs2):
    """
    Determine if a line segment intersects with a parametric cubic spline.
    Returns the intersection details or None if there is no overlap.

    Args:
        lin1 (Line): The line with attributes start_pt and end_pt.
        pcs2 (ParametricCubicSpline): The spline with list_of_outer_points.

    Returns:
        tuple or None: (pcs2.id, outer_left_pt, outer_right_pt, overlap_flag) or None
    """

    def is_point_on_segment(p, start, end):
        """
        Check if point p is on the line segment defined by start and end.
        """
        cross_product = (p[1] - start[1]) * (end[0] - start[0]) - (p[0] - start[0]) * (end[1] - start[1])
        if abs(cross_product) > 1e-6:
            return False  # Not collinear

        dot_product = (p[0] - start[0]) * (end[0] - start[0]) + (p[1] - start[1]) * (end[1] - start[1])
        if dot_product < 0:
            return False  # Beyond start of segment

        squared_length = (end[0] - start[0])**2 + (end[1] - start[1])**2
        if dot_product > squared_length:
            return False  # Beyond end of segment

        return True

    def line_intersection(p1, p2, q1, q2):
        """
        Find intersection between two lines (if any).
        Returns intersection point or None.
        """
        # Line P: p1 + t(p2 - p1)
        # Line Q: q1 + u(q2 - q1)
        # Solve for t and u:
        det = (p2[0] - p1[0]) * (q2[1] - q1[1]) - (p2[1] - p1[1]) * (q2[0] - q1[0])
        if abs(det) < 1e-6:
            return None  # Lines are parallel

        t = ((q1[0] - p1[0]) * (q2[1] - q1[1]) - (q1[1] - p1[1]) * (q2[0] - q1[0])) / det
        u = ((q1[0] - p1[0]) * (p2[1] - p1[1]) - (q1[1] - p1[1]) * (p2[0] - p1[0])) / det

        if 0 <= t <= 1 and 0 <= u <= 1:  # Check if within segment bounds
            intersection_x = p1[0] + t * (p2[0] - p1[0])
            intersection_y = p1[1] + t * (p2[1] - p1[1])
            return (intersection_x, intersection_y)

        return None

    # Prepare output
    intersections = []

    # Iterate through segments of the spline
    for i in range(len(pcs2.list_of_outer_points) - 1):
        p1 = pcs2.list_of_outer_points[i]
        p2 = pcs2.list_of_outer_points[i + 1]
        intersection = line_intersection(lin1.start_pt, lin1.end_pt, p1, p2)
        if intersection:
            intersections.append(intersection)

    # Process intersections
    if not intersections:
        return None

    # Sort intersections by x-coordinate (left-to-right)
    intersections = sorted(intersections, key=lambda pt: pt[0])

    # Determine overlap flag
    overlap_flag = 1 if len(intersections) > 1 else 0

    # Handle touch case
    if len(intersections) == 1:
        intersections.append(intersections[0])  # Duplicate the single point

    outer_left_pt, outer_right_pt = intersections[0], intersections[-1]

    return (pcs2.id, outer_left_pt, outer_right_pt, overlap_flag)
