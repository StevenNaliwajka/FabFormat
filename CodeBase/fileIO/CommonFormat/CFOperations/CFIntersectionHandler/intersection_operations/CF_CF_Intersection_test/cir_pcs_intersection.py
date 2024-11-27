def cir_pcs_intersection(cir1, pcs1):
    # Helper function to calculate the squared distance between two points
    def squared_distance(pt1, pt2):
        return (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2

    # Helper function to check intersection with a radius
    def check_intersection(points, center, radius):
        intersections = []
        for pt in points:
            dist_squared = squared_distance(pt, center)
            if abs(dist_squared - radius ** 2) < 1e-6:  # Approximate touch
                intersections.append((pt, "touch"))
            elif dist_squared < radius ** 2:  # Inside the circle
                intersections.append((pt, "inside"))
        return intersections

    outer_left_pt, outer_right_pt = None, None
    inner_left_pt, inner_right_pt = None, None
    overlap_flag = 0

    # Check intersections with the outer boundary of the circle
    outer_intersections = check_intersection(
        pcs1.list_of_outer_points, cir1.center_pt, cir1.radius
    )

    # Check intersections with the inner boundary of the circle (if exists)
    if cir1.inner_radius:
        inner_intersections = check_intersection(
            pcs1.list_of_outer_points, cir1.center_pt, cir1.inner_radius
        )
    else:
        inner_intersections = []

    # Process outer intersections
    outer_points = [pt for pt, status in outer_intersections if status == "inside"]
    if outer_points:
        overlap_flag = 1
        outer_left_pt, outer_right_pt = sorted(outer_points, key=lambda p: p[0])[:2]

    # Process inner intersections
    inner_points = [pt for pt, status in inner_intersections if status == "inside"]
    if inner_points:
        inner_left_pt, inner_right_pt = sorted(inner_points, key=lambda p: p[0])[:2]

    # Handle cases where shapes touch but do not overlap
    if len(outer_intersections) == 1 and len(inner_intersections) == 1:
        overlap_flag = 0
        if outer_left_pt is None:
            outer_left_pt = inner_left_pt = outer_intersections[0][0]
        if outer_right_pt is None:
            outer_right_pt = inner_right_pt = outer_intersections[0][0]

    return cir1.id, outer_left_pt, outer_right_pt, overlap_flag, inner_left_pt, inner_right_pt
