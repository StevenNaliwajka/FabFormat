def pcs_pcs_intersection(pcs1, pcs2):
    """
    Detects if two parametric cubic splines overlap.

    Parameters:
    pcs1, pcs2: parametric_cubic_spline objects.

    Returns:
    A tuple (pcs1.id, outer_left_pt, outer_right_pt, overlap_flag), or None if no overlap is found.
    """

    def are_points_close(pt1, pt2, tolerance=1e-5):
        """Helper function to check if two points are close within a tolerance."""
        return abs(pt1[0] - pt2[0]) < tolerance and abs(pt1[1] - pt2[1]) < tolerance

    # Extract points from the splines
    points1 = pcs1.list_of_outer_points
    points2 = pcs2.list_of_outer_points

    # Initialize variables to store intersection points and the overlap flag
    outer_left_pt = None
    outer_right_pt = None
    overlap_flag = 0

    # Check for intersections
    for pt1 in points1:
        for pt2 in points2:
            if are_points_close(pt1, pt2):
                if not outer_left_pt:
                    # First intersection point found
                    outer_left_pt = pt1
                elif not outer_right_pt or pt1 != outer_left_pt:
                    # Second intersection point found
                    outer_right_pt = pt1

    # Determine overlap flag
    if outer_left_pt and outer_right_pt:
        overlap_flag = 1
    elif outer_left_pt and not outer_right_pt:
        outer_right_pt = outer_left_pt

    # If no intersections are found, return None
    if not outer_left_pt:
        return None

    return (pcs1.id, outer_left_pt, outer_right_pt, overlap_flag)
