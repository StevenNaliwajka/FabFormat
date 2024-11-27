def fsa_pcs_intersection(fsa1, pcs1):
    """
    Detect intersection between a filled symmetrical arc and a parametric cubic spline.

    Parameters:
        fsa1: The filled symmetrical arc object.
        pcs1: The parametric cubic spline object.

    Returns:
        Tuple: (fsa1.id, outer_left_pt, outer_right_pt, overlap_flag, inner_left_pt, inner_right_pt)
               or None if no intersection.
    """

    def point_in_arc(pt, center, radius, start_angle, end_angle):
        """Check if a point lies within a specified arc range and radius."""
        dx, dy = pt[0] - center[0], pt[1] - center[1]
        distance_squared = dx ** 2 + dy ** 2
        angle = math.atan2(dy, dx) % (2 * math.pi)
        in_radius = distance_squared <= radius ** 2
        in_angle = start_angle <= angle <= end_angle
        return in_radius and in_angle

    def find_intersection_with_arc(points, center, radius, start_angle, end_angle):
        """Find intersections of points with an arc."""
        intersections = []
        for pt in points:
            if point_in_arc(pt, center, radius, start_angle, end_angle):
                intersections.append(pt)
        return intersections

    import math

    # Define the start and end angles of the symmetrical arc
    start_angle = math.atan2(fsa1.start_pt[1] - fsa1.center_pt[1],
                             fsa1.start_pt[0] - fsa1.center_pt[0]) % (2 * math.pi)
    end_angle = math.atan2(fsa1.end_pt[1] - fsa1.center_pt[1],
                           fsa1.end_pt[0] - fsa1.center_pt[0]) % (2 * math.pi)

    # Ensure the angle range is correctly handled
    if start_angle > end_angle:
        start_angle, end_angle = end_angle, start_angle

    outer_intersections = find_intersection_with_arc(
        pcs1.list_of_outer_points, fsa1.center_pt, fsa1.arc_radius, start_angle, end_angle
    )

    inner_intersections = []
    if fsa1.inner_radius and fsa1.inner_radius > 0:
        inner_intersections = find_intersection_with_arc(
            pcs1.list_of_outer_points, fsa1.center_pt, fsa1.inner_radius, start_angle, end_angle
        )

    # Determine overlap
    overlap_flag = 0
    if outer_intersections or inner_intersections:
        overlap_flag = 1

    # Sort intersections to find the "left" and "right" points
    outer_left_pt = outer_intersections[0] if outer_intersections else None
    outer_right_pt = outer_intersections[-1] if outer_intersections else None

    inner_left_pt = inner_intersections[0] if inner_intersections else None
    inner_right_pt = inner_intersections[-1] if inner_intersections else None

    if not outer_intersections and not inner_intersections:
        return None  # No intersection detected

    return (
        fsa1.id, outer_left_pt, outer_right_pt, overlap_flag, inner_left_pt, inner_right_pt
    )
