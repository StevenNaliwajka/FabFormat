def fsa_sap_intersection(fsa1, sap2):
    """
    Detect if a filled symmetrical arc (fsa1) and a symmetrical arc (sap2) overlap.
    Return the intersection points and flags.
    """

    def find_intersection(arc_points, sap_points):
        """Helper function to find intersections between two sets of points."""
        intersections = []
        for pt in arc_points:
            if pt in sap_points:
                intersections.append(pt)
        return intersections

    # Extract relevant data
    outer_points_fsa = fsa1.list_of_outer_points
    inner_points_fsa = getattr(fsa1, 'list_of_inner_points', [])
    sap_points = sap2.list_of_outer_points

    # Check outer boundary intersection
    outer_intersections = find_intersection(outer_points_fsa, sap_points)
    outer_flag = 1 if len(outer_intersections) > 1 else 0

    # Check inner boundary intersection (if exists)
    if inner_points_fsa:
        inner_intersections = find_intersection(inner_points_fsa, sap_points)
        inner_flag = 1 if len(inner_intersections) > 1 else 0
    else:
        inner_intersections = []
        inner_flag = 0

    # Determine overlap type
    if not outer_intersections and not inner_intersections:
        return None  # No overlap

    # Outer points: left and right
    if outer_intersections:
        outer_left_pt = min(outer_intersections, key=lambda p: p[0])  # Smallest x-coordinate
        outer_right_pt = max(outer_intersections, key=lambda p: p[0])  # Largest x-coordinate
    else:
        outer_left_pt = outer_right_pt = None

    # Inner points: left and right
    if inner_intersections:
        inner_left_pt = min(inner_intersections, key=lambda p: p[0])  # Smallest x-coordinate
        inner_right_pt = max(inner_intersections, key=lambda p: p[0])  # Largest x-coordinate
    else:
        inner_left_pt = inner_right_pt = None

    # Return results
    return fsa1.id, outer_left_pt, outer_right_pt, outer_flag, inner_left_pt, inner_right_pt
