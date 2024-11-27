import math

def cir_lin_intersection(cir1, lin1):
    def point_on_segment(pt, start_pt, end_pt):
        """Check if a point lies on a line segment."""
        return (
            min(start_pt[0], end_pt[0]) <= pt[0] <= max(start_pt[0], end_pt[0])
            and min(start_pt[1], end_pt[1]) <= pt[1] <= max(start_pt[1], end_pt[1])
        )

    def line_circle_intersections(center, radius, start_pt, end_pt):
        """Compute intersection points of a line segment with a circle."""
        cx, cy = center
        x1, y1 = start_pt
        x2, y2 = end_pt

        # Line equation: ax + by + c = 0
        dx, dy = x2 - x1, y2 - y1
        a = dx ** 2 + dy ** 2
        b = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
        c = (x1 - cx) ** 2 + (y1 - cy) ** 2 - radius ** 2

        # Quadratic formula discriminant
        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return []  # No intersection

        # Calculate intersection points
        sqrt_discriminant = math.sqrt(discriminant)
        t1 = (-b + sqrt_discriminant) / (2 * a)
        t2 = (-b - sqrt_discriminant) / (2 * a)

        intersections = []
        for t in (t1, t2):
            if 0 <= t <= 1:  # Check if within segment bounds
                ix, iy = x1 + t * dx, y1 + t * dy
                intersections.append((ix, iy))
        return intersections

    # Check intersections with the outer radius
    outer_intersections = line_circle_intersections(
        cir1.center_pt, cir1.radius, lin1.start_pt, lin1.end_pt
    )

    # Check intersections with the inner radius if it exists
    inner_intersections = []
    if hasattr(cir1, 'inner_radius') and cir1.inner_radius:
        inner_intersections = line_circle_intersections(
            cir1.center_pt, cir1.inner_radius, lin1.start_pt, lin1.end_pt
        )

    # Handle overlap conditions
    def process_intersections(intersections):
        if not intersections:
            return None, None, 0  # No overlap
        intersections = sorted(intersections)  # Sort to get left and right
        if len(intersections) == 1:  # Tangent case
            return intersections[0], intersections[0], 0
        return intersections[0], intersections[1], 1

    outer_left_pt, outer_right_pt, outer_flag = process_intersections(
        outer_intersections
    )
    inner_left_pt, inner_right_pt, inner_flag = process_intersections(
        inner_intersections
    )

    # If no intersections, return None
    if outer_flag == 0 and inner_flag == 0:
        return None

    return (
        cir1.id,
        outer_left_pt,
        outer_right_pt,
        outer_flag,
        inner_left_pt,
        inner_right_pt,
    )
