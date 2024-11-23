import math


def get_cf_symmetrical_arc_radius_point(degree, start, center, radius):
    """
    Calculate the point on an arc at half the given degree.

    Parameters:
    - degree: float, the total degree of the arc
    - start: tuple (x_s, y_s), the start point of the arc
    - center: tuple (x_c, y_c), the center of the arc
    - radius: float, the radius of the arc

    Returns:
    - midpoint: tuple (x, y), the coordinates of the point on the arc at half the degree
    """
    # Calculate half the angle in degrees
    half_angle_deg = degree / 2

    # Convert to radians
    half_angle_rad = math.radians(half_angle_deg)

    # Vector from center to start
    x_s, y_s = start
    x_c, y_c = center
    v1 = (x_s - x_c, y_s - y_c)

    # Length of the vector (should match the radius)
    mag_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)

    # Unit vector in the direction of v1
    unit_v1 = (v1[0] / mag_v1, v1[1] / mag_v1)

    # Rotate the unit vector by half the angle
    cos_half_angle = math.cos(half_angle_rad)
    sin_half_angle = math.sin(half_angle_rad)

    # Rotation formula
    rotated_x = unit_v1[0] * cos_half_angle - unit_v1[1] * sin_half_angle
    rotated_y = unit_v1[0] * sin_half_angle + unit_v1[1] * cos_half_angle

    # Scale by radius to get the point on the arc
    midpoint_x = x_c + rotated_x * radius
    midpoint_y = y_c + rotated_y * radius

    return midpoint_x, midpoint_y


def calculate_sym_arc_degree(start, end, center):
    """
    Calculate the degree of an arc given the start, end, and center coordinates.

    Parameters:
    - start: tuple (x_s, y_s), the start point of the arc
    - end: tuple (x_e, y_e), the end point of the arc
    - center: tuple (x_c, y_c), the center of rotation

    Returns:
    - arc_degree: float, the degree of the arc
    """
    # Extract coordinates
    x_s, y_s = start
    x_e, y_e = end
    x_c, y_c = center

    # Vectors from the center to the start and end points
    v1 = (x_s - x_c, y_s - y_c)
    v2 = (x_e - x_c, y_e - y_c)

    # Dot product of v1 and v2
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]

    # Magnitudes of v1 and v2
    mag_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    mag_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    # Cosine of the angle
    cos_theta = dot_product / (mag_v1 * mag_v2)

    # Clamp cos_theta to avoid numerical errors
    cos_theta = max(-1, min(1, cos_theta))

    # Angle in radians
    theta_rad = math.acos(cos_theta)

    # Convert to degrees
    theta_deg = math.degrees(theta_rad)

    # Cross product to determine orientation
    cross_product = v1[0] * v2[1] - v1[1] * v2[0]

    # Adjust for clockwise or counterclockwise
    if cross_product < 0:  # Clockwise
        theta_deg = 360 - theta_deg

    return theta_deg