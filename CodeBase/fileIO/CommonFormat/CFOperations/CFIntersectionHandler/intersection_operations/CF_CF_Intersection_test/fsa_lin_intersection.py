def fsa_lin_intersection(fsa1, lin1):
    """
    Detects overlap or intersection between a filled symmetrical arc and a line.

    Parameters:
    - fsa1: A filled symmetrical arc object.
    - lin1: A line object.

    Returns:
    - A tuple: (fsa1.id, outer_left_pt, outer_right_pt, overlap_flag, inner_left_pt, inner_right_pt)
    """

    def point_on_line(pt, line):
        """Check if a point lies on the line segment."""
        x, y = pt
        x1, y1 = line.start_pt
        x2, y2 = line.end_pt
        # Check if point is within line bounds
        return (
                min(x1, x2) <= x <= max(x1, x2) and
                min(y1, y2) <= y <= max(y1, y2)
        )

    def line_circle_intersection(center, radius, line):
        """Calculate intersection points of a line and a circle."""
        x1, y1 = line.start_pt
        x2, y2 = line.end_pt
        cx, cy = center

        # Line parameters
        dx = x2 - x1
        dy = y2 - y1

        # Quadratic formula coefficients
        A = dx ** 2 + dy ** 2
        B = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
        C = (x1 - cx) ** 2 + (y1 - cy) ** 2 - radius ** 2

        # Discriminant
        D = B ** 2 - 4 * A * C

        if D < 0:
            return []  # No intersection
        elif D == 0:
            # One intersection point (tangent)
            t = -B / (2 * A)
            ix = x1 + t * dx
            iy = y1 + t * dy
            if point_on_line((ix, iy), line):
                return [(ix, iy)]
            return []
        else:
            # Two intersection points
            sqrt_D = D ** 0.5
            t1 = (-B + sqrt_D) / (2 * A)
            t2 = (-B - sqrt_D) / (2 * A)

            # Check if the points are on the line segment
            intersections = []
            for t in (t1, t2):
                ix = x1 + t * dx
                iy = y1 + t * dy
                if point_on_line((ix, iy), line):
                    intersections.append((ix, iy))
            return intersections

    # Initialize result variables
    outer_left_pt = None
    outer_right_pt = None
    inner_left_pt = None
    inner_right_pt = None
    overlap_flag = 0

    # Check intersections with the outer arc
    outer_intersections = line_circle_intersection(fsa1.center_pt, fsa1.arc_radius, lin1)
    if outer_intersections:
        outer_left_pt = min(outer_intersections)
        outer_right_pt = max(outer_intersections)
        overlap_flag = 1

    # Check intersections with the inner arc if applicable
    if fsa1.inner_radius:
        inner_intersections = line_circle_intersection(fsa1.center_pt, fsa1.inner_radius, lin1)
        if inner_intersections:
            inner_left_pt = min(inner_intersections)
            inner_right_pt = max(inner_intersections)
            overlap_flag = 1

    # Handle the case of touching at a single point
    if outer_left_pt == outer_right_pt:
        outer_right_pt = outer_left_pt

    if inner_left_pt == inner_right_pt:
        inner_right_pt = inner_left_pt

    return fsa1.id, outer_left_pt, outer_right_pt, overlap_flag, inner_left_pt, inner_right_pt
