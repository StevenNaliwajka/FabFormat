def sap_sap_intersection(sap1, sap2):
    # Step 1: Check if arcs' bounding boxes overlap (already done, per your description).

    # Step 2: Verify arcs are close enough for potential intersection.
    if abs(sap1.edge_radius - sap2.edge_radius) > sap1.arc_radius + sap2.arc_radius:
        return None

    # Helper function to determine if a point is within an arc's angular range.
    def is_point_in_arc_range(center, start, end, point):
        def angle_between(p1, p2):
            from math import atan2, degrees
            return (degrees(atan2(p2[1] - p1[1], p2[0] - p1[0])) + 360) % 360

        angle_start = angle_between(center, start)
        angle_end = angle_between(center, end)
        angle_point = angle_between(center, point)

        if angle_start < angle_end:
            return angle_start <= angle_point <= angle_end
        return angle_point >= angle_start or angle_point <= angle_end

    # Step 3: Check for intersections by iterating through outer points of sap1 and sap2.
    intersections = []
    for point1 in sap1.list_of_outer_points:
        for point2 in sap2.list_of_outer_points:
            # Check if the distance between points is within a small tolerance (they touch).
            if abs(point1[0] - point2[0]) < 1e-6 and abs(point1[1] - point2[1]) < 1e-6:
                if is_point_in_arc_range(sap1.center_pt, sap1.start_pt, sap1.end_pt, point1) and \
                        is_point_in_arc_range(sap2.center_pt, sap2.start_pt, sap2.end_pt, point2):
                    intersections.append(point1)

    # Step 4: Determine overlap flag and results.
    if len(intersections) == 0:
        return None
    elif len(intersections) == 1:
        outer_left_pt = intersections[0]
        outer_right_pt = intersections[0]
        overlap_flag = 0  # Touches without overlapping.
    else:
        intersections = sorted(intersections, key=lambda pt: (pt[0], pt[1]))
        outer_left_pt = intersections[0]
        outer_right_pt = intersections[-1]
        overlap_flag = 1  # Overlaps.

    return sap1.id, outer_left_pt, outer_right_pt, overlap_flag
