import math


def pcs_sap_intersection(pcs1, sap):
    def is_point_on_arc(point, sap):
        """Check if a point lies on the arc."""
        cx, cy = sap.center_pt
        px, py = point
        distance = ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
        if abs(distance - sap.arc_radius) > 1e-6:  # Check radial distance
            return False
        # Check angular position
        angle = math.atan2(py - cy, px - cx) * 180 / math.pi
        start_angle = math.atan2(sap.start_pt[1] - cy, sap.start_pt[0] - cx) * 180 / math.pi
        end_angle = math.atan2(sap.end_pt[1] - cy, sap.end_pt[0] - cx) * 180 / math.pi
        if start_angle < end_angle:
            return start_angle <= angle <= end_angle
        else:  # Handle arc spanning 0 degrees
            return angle >= start_angle or angle <= end_angle

    def line_intersection(p1, p2, q1, q2):
        """Find intersection between two line segments."""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = q1
        x4, y4 = q2

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None  # Parallel lines

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        if 0 <= t <= 1 and 0 <= u <= 1:
            ix = x1 + t * (x2 - x1)
            iy = y1 + t * (y2 - y1)
            return ix, iy
        return None

    intersections = []
    for i in range(len(pcs1.list_of_outer_points) - 1):
        p1, p2 = pcs1.list_of_outer_points[i], pcs1.list_of_outer_points[i + 1]
        for j in range(len(sap.list_of_outer_points) - 1):
            q1, q2 = sap.list_of_outer_points[j], sap.list_of_outer_points[j + 1]
            intersect = line_intersection(p1, p2, q1, q2)
            if intersect and is_point_on_arc(intersect, sap):
                intersections.append(intersect)

    if not intersections:
        return None

    intersections = sorted(intersections, key=lambda pt: pt[0])  # Sort by x-coordinate
    outer_left_pt = intersections[0]
    outer_right_pt = intersections[-1]
    overlap_flag = 1 if len(intersections) > 1 else 0

    return pcs1.id, outer_left_pt, outer_right_pt, overlap_flag
