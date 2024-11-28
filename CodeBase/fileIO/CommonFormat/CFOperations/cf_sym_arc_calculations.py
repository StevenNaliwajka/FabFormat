import math

from CodeBase.fileIO.CommonFormat.CFOperations.GeneralMath.calculate_arc_radians import calculate_arc_radians


def get_cf_symmetrical_arc_radius_point(degree, start_pt, center_pt, radius):
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
    x_s, y_s = start_pt
    x_c, y_c = center_pt
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


def find_sym_arc_radius(center, point, new_distance):
    # takes a center and a point and converts to a vector.
    # normalizes the vector and multiplies by the new distance.

    # Calculate the vector from the center to the point
    vector = (point[0] - center[0], point[1] - center[1])

    # Calculate the magnitude of the vector
    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)

    # Normalize the vector
    unit_vector = (vector[0] / magnitude, vector[1] / magnitude)

    # Scale the vector by the new distance
    scaled_vector = (unit_vector[0] * new_distance, unit_vector[1] * new_distance)

    # Calculate the new point
    new_point = (center[0] + scaled_vector[0], center[1] + scaled_vector[1])

    return new_point

def generate_points_on_sym_arc_complex(self):
    # Reference CF shapes documentation "Sym_arc_pt_1.jpg" + "Sym_arc_pt_2.jpg"
    num_points = self.qty_points_on_curve

    edge_radius = self.edge_radius
    amplitude = self.arc_radius
    x_rad = calculate_arc_radians(self.center_pt, self.start_pt)
    z_rad = calculate_arc_radians(self.center_pt, self.end_pt)

    step = (z_rad - x_rad) / (num_points - 1)  # Calculate the step size
    theta_list = [x_rad + i * step for i in range(num_points)]

    points_on_curve = []
    for theta in theta_list:
        x = (edge_radius + amplitude * math.sin(math.pi/(x_rad-z_rad)*(x_rad-theta))) * math.cos(theta)
        y = (edge_radius + amplitude * math.sin(math.pi / (x_rad - z_rad) * (x_rad - theta))) * math.sin(theta)

        shifted_y = x + self.center_pt[0]
        shifted_x = y + self.center_pt[1]
        points_on_curve.append((shifted_x, shifted_y))
    return points_on_curve
