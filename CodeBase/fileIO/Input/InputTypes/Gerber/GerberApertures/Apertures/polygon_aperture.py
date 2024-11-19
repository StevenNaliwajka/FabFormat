import math

from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_symmetrical_arc_trace import CFSymmetricalArcTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent
from math import sqrt


class PolygonAperture(ApertureParent):
    def __init__(self, ap_number, center_x, center_y, outer_diameter, num_vertices, rotation, unit, inside_hole_diam=None):
        # See Page 55:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy

        # Sorry for this one. 110% can be improved.
        # Garuneed issue in complex_polygon_to_cf if the rotation is above like 50 degrees or something...
        # the arcs are not rotated aswell which cause issues from using fixed points...

        super().__init__(unit)
        self.aperture_type = "c"
        self.aperture_number = ap_number
        self.center_x = center_x
        self.center_y = center_y
        self.outer_diameter = outer_diameter
        if num_vertices < 3 or num_vertices > 12:
            raise ValueError(f"PolygonAperture: Num_Vertices are incorrect, {num_vertices} is an unacceptable number.")
        self.num_vertices = num_vertices
        self.rotation = rotation
        self.inner_hole_diameter = inside_hole_diam

        self.degree_per_vertice = 360 / num_vertices

        self.to_common_form()

    def to_common_form(self):
        # Determine rotation
        #  to rad
        angle_rad = math.radians(self.rotation)
        # get sin and cosin value.
        cosine_value = math.cos(angle_rad)
        sine_value = math.sin(angle_rad)
        starting_x = (cosine_value*self.outer_diameter/2) + self.center_x
        starting_y = (sine_value * self.outer_diameter / 2) + self.center_y
        if self.inner_hole_diameter:
            self.complex_polygon_to_cf(starting_x, starting_y)
        else:
            self.polygon_to_cf(starting_x, starting_y)

    def polygon_to_cf(self, starting_x, starting_y):
        # Creates One polygon
        trace_list_polygon = []

        angle_deg = 0
        # adds point zero
        trace_list_polygon.append((starting_x, starting_y))

        # Iterate through every point on polygon
        counter = 1
        while counter <= self.num_vertices:
            # get angle degree
            angle_deg = (self.degree_per_vertice * counter) + self.rotation
            # conv to rad
            angle_rad = math.radians(angle_deg)

            # get sin and cosin value.
            cosine_value = math.cos(angle_rad)
            sine_value = math.sin(angle_rad)
            # get real x and y value
            x_pos = (cosine_value * self.outer_diameter / 2) + self.center_x
            y_pos = (sine_value * self.outer_diameter / 2) + self.center_y
            # add trace
            trace_list_polygon.append((x_pos, y_pos))
            counter += 1
        self.common_form.append(CFPolygonTrace(trace_list_polygon))

    def complex_polygon_to_cf(self, starting_x, starting_y):
        # Creates 4 arcs, 2 polygons=

        # Determine smallest axis
        smallest = self.inner_hole_diameter / 2
        # Solve for arc length
        arc_len = sqrt((smallest ** 2) + (smallest ** 2)) - smallest

        corner_offsets = [
            (-smallest, -smallest),
            (-smallest, smallest),
            (smallest, smallest),
            (smallest, -smallest)
        ]

        for offset_x, offset_y in corner_offsets:
            # Apply center offset to start and end points
            s_x = self.center_x + (offset_x if offset_y == -smallest else 0)
            s_y = self.center_y + (0 if offset_x == -smallest else offset_y)
            e_x = self.center_x + (0 if offset_y == -smallest else offset_x)
            e_y = self.center_y + (offset_y if offset_x == -smallest else 0)

            # Append the arc trace, centered around (center_x, center_y)
            self.common_form.append(
                CFSymmetricalArcTrace(
                    self.center_x + offset_x,  # Adjusted center offset
                    self.center_y + offset_y,  # Adjusted center offset
                    s_x,
                    s_y,
                    e_x,
                    e_y,
                    arc_len
                )
            )

        # Creates Two polygons
        trace_list_polygon = []
        trace_list_second_polygon = []
        angle_deg = 0
        # adds point zero
        trace_list_polygon.append((starting_x, starting_y))

        # Determine split point: the first half gets the larger part if the size is odd
        split_point = (self.num_vertices + 1) // 2  # This ensures the first half is larger for odd n

        # First half indices
        half1_indices = list(range(split_point))

        # Second half indices (overlaps the last index of the first half)
        half2_indices = list(range(split_point - 1, self.num_vertices)) + [0]

        # First half of outer points
        for i in half1_indices:
            # get angle degree
            angle_deg = (self.degree_per_vertice * i) + self.rotation
            # conv to rad
            angle_rad = math.radians(angle_deg)

            # get sin and cosin value.
            cosine_value = math.cos(angle_rad)
            sine_value = math.sin(angle_rad)
            # get real x and y value
            x_pos = (cosine_value * self.outer_diameter / 2) + self.center_x
            y_pos = (sine_value * self.outer_diameter / 2) + self.center_y
            # add trace
            trace_list_polygon.append((x_pos, y_pos))

        # top left of arcs cord
        trace_list_polygon.append(((-(self.inner_hole_diameter/2)+self.center_x), (self.inner_hole_diameter/2+self.center_y)))
        # top right of arcs cord
        trace_list_polygon.append((((self.inner_hole_diameter / 2) + self.center_x), (self.inner_hole_diameter / 2) + self.center_y))
        # Starting cord
        trace_list_polygon.append((starting_x, starting_y))

        # Create First polygon
        # I KINDA BUILT THIS LIKE AIDS....
        # COULD BE IMPROVED
        new_list = self.flatten_traces(trace_list_polygon)
        new_polygon = CFPolygonTrace(new_list)
        self.common_form.append(new_polygon)

        # Second polygon
        # Starting cord
        trace_list_second_polygon.append((starting_x, starting_y))
        # top right of arcs cord
        trace_list_second_polygon.append((self.inner_hole_diameter / 2, self.inner_hole_diameter / 2))
        # bottom right of arcs cord
        trace_list_second_polygon.append(((-self.inner_hole_diameter / 2), self.inner_hole_diameter / 2))
        # bottom left of arcs cord
        trace_list_second_polygon.append(((-self.inner_hole_diameter / 2), -self.inner_hole_diameter / 2))
        # top left of arcs cord
        trace_list_second_polygon.append((-(self.inner_hole_diameter / 2), self.inner_hole_diameter / 2))
        for i in half2_indices:
            # get angle degree
            angle_deg = (self.degree_per_vertice * i) + self.rotation
            # conv to rad
            angle_rad = math.radians(angle_deg)

            # get sin and cosin value.
            cosine_value = math.cos(angle_rad)
            sine_value = math.sin(angle_rad)
            # get real x and y value
            x_pos = (cosine_value * self.outer_diameter / 2) + self.center_x
            y_pos = (sine_value * self.outer_diameter / 2) + self.center_y
            # add trace
            trace_list_second_polygon.append((x_pos, y_pos))
        new_list = self.flatten_traces(trace_list_second_polygon)
        new_polygon = CFPolygonTrace(new_list)
        self.common_form.append(new_polygon)

    def flatten_traces(self, trace_list):
        return [coord for pair in trace_list for coord in pair]