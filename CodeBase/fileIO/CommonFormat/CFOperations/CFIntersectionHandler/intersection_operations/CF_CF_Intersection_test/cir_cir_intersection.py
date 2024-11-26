import math

# UPDATE TO HANDLE THE INNER LINE VS OUTER LINE OVERLAPS
def cir_cir_intersection(cir1, cir2):
    # Extract circle attributes
    c1_center, c1_outer, c1_inner = cir1.center_pt, cir1.radius, getattr(cir1, 'inner_radius', 0)
    c2_center, c2_outer, c2_inner = cir2.center_pt, cir2.radius, getattr(cir2, 'inner_radius', 0)

    # Calculate distance between centers
    dx = c2_center[0] - c1_center[0]
    dy = c2_center[1] - c1_center[1]
    center_distance = math.sqrt(dx ** 2 + dy ** 2)

    # Check bounding scenarios
    if center_distance > c1_outer + c2_outer:  # Circles are too far apart
        return None
    if center_distance < abs(c1_inner - c2_outer):  # One circle is entirely inside the other without touching
        return None

    # Determine overlap_flag
    overlap_flag = 1 if center_distance < c1_outer + c2_outer and center_distance > abs(c1_inner - c2_outer) else 0

    # Calculate intersection points (if they exist)
    if center_distance == 0:  # Same center, potentially concentric
        return None

    # Find the intersection points between the outer radii
    a = (c1_outer ** 2 - c2_outer ** 2 + center_distance ** 2) / (2 * center_distance)
    h = math.sqrt(max(c1_outer ** 2 - a ** 2, 0))

    # Midpoint between the circle centers along the line of intersection
    mid_x = c1_center[0] + a * dx / center_distance
    mid_y = c1_center[1] + a * dy / center_distance

    # Offset intersection points perpendicular to the line between centers
    inter1_x = mid_x + h * dy / center_distance
    inter1_y = mid_y - h * dx / center_distance
    inter2_x = mid_x - h * dy / center_distance
    inter2_y = mid_y + h * dx / center_distance

    left_pt = (inter1_x, inter1_y) if inter1_x < inter2_x else (inter2_x, inter2_y)
    right_pt = (inter2_x, inter2_y) if inter1_x < inter2_x else (inter1_x, inter1_y)

    # Handle touching cases
    if center_distance == c1_outer + c2_outer or center_distance == abs(c1_inner - c2_outer):
        left_pt = right_pt = (mid_x, mid_y)

    return (cir1.id, left_pt, right_pt, overlap_flag)
