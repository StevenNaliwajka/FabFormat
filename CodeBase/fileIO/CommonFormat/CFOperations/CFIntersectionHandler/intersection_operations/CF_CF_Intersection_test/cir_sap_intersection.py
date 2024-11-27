def cir_sap_intersection(cir1, sap1):
    """
    Determines if a Circle and a Symmetrical Arc intersect and provides details of the intersection.

    Parameters:
    cir1 (Circle): The circle object.
    sap1 (SymmetricalArc): The symmetrical arc object.

    Returns:
    tuple: (cir1.id, outer_left_pt, outer_right_pt, overlap_flag, inner_left_pt, inner_right_pt)
           outer_left_pt and outer_right_pt are the points of intersection on the outer circle.
           inner_left_pt and inner_right_pt are the points of intersection on the inner circle (if applicable).
           overlap_flag is 1 if the shapes overlap, 0 if they bound but do not overlap.
           If no intersection, return None.
    """
    from math import sqrt, atan2, degrees

    def distance(pt1, pt2):
        """Calculate Euclidean distance between two points."""
        return sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    def is_point_on_arc(pt, sap):
        """Check if a point lies on the arc."""
        dist_to_center = distance(pt, sap.center_pt)
        if not (sap.edge_radius <= dist_to_center <= sap.arc_radius):
            return False

        angle = degrees(atan2(pt[1] - sap.center_pt[1], pt[0] - sap.center_pt[0]))
        start_angle = degrees(atan2(sap.start_pt[1] - sap.center_pt[1], sap.start_pt[0] - sap.center_pt[0]))
        end_angle = degrees(atan2(sap.end_pt[1] - sap.center_pt[1], sap.end_pt[0] - sap.center_pt[0]))

        # Normalize angles
        angle = (angle + 360) % 360
        start_angle = (start_angle + 360) % 360
        end_angle = (end_angle + 360) % 360

        if start_angle <= end_angle:
            return start_angle <= angle <= end_angle
        else:
            return angle >= start_angle or angle <= end_angle

    def find_circle_arc_intersections(circle, arc, radius=None):
        """Find intersection points between a circle and an arc."""
        radius = radius if radius else circle.radius  # Use provided radius or default to outer radius
        intersections = []
        for pt in arc.list_of_outer_points:
            if distance(circle.center_pt, pt) <= radius:
                if is_point_on_arc(pt, arc):
                    intersections.append(pt)
        return intersections

    # Outer circle intersection with arc
    outer_intersections = find_circle_arc_intersections(cir1, sap1)
    outer_left_pt, outer_right_pt = (None, None)
    if len(outer_intersections) >= 1:
        outer_left_pt = min(outer_intersections, key=lambda p: p[0])  # Leftmost point
        outer_right_pt = max(outer_intersections, key=lambda p: p[0])  # Rightmost point

    # Inner circle intersection with arc (if applicable)
    inner_left_pt, inner_right_pt = (None, None)
    if hasattr(cir1, 'inner_radius') and cir1.inner_radius:
        inner_intersections = find_circle_arc_intersections(cir1, sap1, radius=cir1.inner_radius)
        if len(inner_intersections) >= 1:
            inner_left_pt = min(inner_intersections, key=lambda p: p[0])  # Leftmost point
            inner_right_pt = max(inner_intersections, key=lambda p: p[0])  # Rightmost point

    # Determine overlap_flag
    overlap_flag = 0
    if outer_left_pt and outer_right_pt and inner_left_pt and inner_right_pt:
        overlap_flag = 1  # Shapes overlap
    elif outer_left_pt and outer_right_pt:
        overlap_flag = 0  # Bound but do not overlap

    # Return result
    if not outer_left_pt and not inner_left_pt:
        return None  # No intersection
    return cir1.id, outer_left_pt, outer_right_pt, overlap_flag, inner_left_pt, inner_right_pt
