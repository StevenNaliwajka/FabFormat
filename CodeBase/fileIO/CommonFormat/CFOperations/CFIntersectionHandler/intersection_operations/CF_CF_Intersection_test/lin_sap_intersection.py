def lin_sap_intersection(lin1, sap1):
    # Helper function to calculate the squared distance between two points
    def distance_squared(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    # Helper function to check if a point is on a line segment
    def point_on_line_segment(pt, line_start, line_end):
        cross_product = (pt[1] - line_start[1]) * (line_end[0] - line_start[0]) - \
                        (pt[0] - line_start[0]) * (line_end[1] - line_start[1])
        if abs(cross_product) > 1e-7:  # Allow for small floating-point errors
            return False
        dot_product = (pt[0] - line_start[0]) * (line_end[0] - line_start[0]) + \
                      (pt[1] - line_start[1]) * (line_end[1] - line_start[1])
        if dot_product < 0:
            return False
        squared_length = distance_squared(line_start, line_end)
        return dot_product <= squared_length

    # Step 1: Check intersection of the line with the arc's radius
    intersections = []
    for outer_pt in sap1.list_of_outer_points:
        # Calculate if line intersects this outer point of the arc
        a = distance_squared(lin1.start_pt, lin1.end_pt)
        b = 2 * ((lin1.end_pt[0] - lin1.start_pt[0]) * (lin1.start_pt[0] - outer_pt[0]) +
                 (lin1.end_pt[1] - lin1.start_pt[1]) * (lin1.start_pt[1] - outer_pt[1]))
        c = distance_squared(outer_pt, sap1.center_pt) - sap1.arc_radius ** 2
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            continue  # No intersection for this segment

        sqrt_discriminant = discriminant ** 0.5
        t1 = (-b + sqrt_discriminant) / (2 * a)
        t2 = (-b - sqrt_discriminant) / (2 * a)

        for t in (t1, t2):
            if 0 <= t <= 1:  # Ensure the intersection lies on the segment
                intersection_pt = (lin1.start_pt[0] + t * (lin1.end_pt[0] - lin1.start_pt[0]),
                                   lin1.start_pt[1] + t * (lin1.end_pt[1] - lin1.start_pt[1]))
                if point_on_line_segment(intersection_pt, sap1.start_pt, sap1.end_pt):
                    intersections.append(intersection_pt)

    # Step 2: Determine overlap_flag and intersections
    if not intersections:
        return None  # No intersections

    intersections = sorted(intersections)  # Sort points for left-to-right ordering
    outer_left_pt = intersections[0]
    outer_right_pt = intersections[-1]

    overlap_flag = 1 if len(intersections) > 1 else 0
    if len(intersections) == 1 and distance_squared(outer_left_pt, outer_right_pt) == 0:
        overlap_flag = 0  # Touches but no overlap

    return sap1.id, outer_left_pt, outer_right_pt, overlap_flag
