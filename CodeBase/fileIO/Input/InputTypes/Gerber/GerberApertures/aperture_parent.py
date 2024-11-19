from abc import abstractmethod
from math import sqrt

from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_symmetrical_arc_trace import CFSymmetricalArcTrace


class ApertureParent:
    def __init__(self, unit):
        self.aperture_type = None
        self.aperture_number = None
        self.inner_hole_diameter = None
        self.common_form = []
        self.unit = unit

    # Comparison function to make objects comparable based on aperture_number
    def __lt__(self, other):
        return self.aperture_number < other.aperture_number

    @abstractmethod
    def to_common_form(self, *args, **kwargs):
        pass

    def rectangle_to_cf(self, center_x, center_y, x_size, y_size):
        # Creates 1 CF polygon: EZ
        point_list = []
        # BL: BOTTOM LEFT
        # BR: BOTTOM RIGHT
        # TL: TOP LEFT
        # TR: TOP RIGHT
        # BL
        current_x = center_x - (x_size / 2)
        current_y = center_y - (y_size / 2)
        point_list.append(current_x)
        point_list.append(current_y)
        # TL
        current_y = current_y + y_size
        point_list.append(current_x)
        point_list.append(current_y)
        # TR
        current_x = current_x + x_size
        point_list.append(current_x)
        point_list.append(current_y)
        # BR
        current_y = current_y - y_size
        point_list.append(current_x)
        point_list.append(current_y)
        # BLx2
        current_x = current_x - x_size
        point_list.append(current_x)
        point_list.append(current_y)

        new_common_form = CFPolygonTrace(self.unit, point_list)
        self.common_form.append(new_common_form)

    def create_corner_arcs_and_inside_circle(self, center_x, center_y, x_size, y_size, inside_hole_diam):
        # Used by Complex Rectangle and Complex Obround
        # Complex Rectangle: #1,2,3,4,5
        # Complex Obround: #1,2,3,4,5

        # Determine smallest axis
        smallest = min(x_size, y_size)
        # In complex variation, Create Circle #1
        self.common_form.append(CFCircleTrace(self.unit, center_x, center_y, smallest, inside_hole_diam))

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
            s_x = center_x + (offset_x if offset_y == -smallest else 0)
            s_y = center_y + (0 if offset_x == -smallest else offset_y)
            e_x = center_x + (0 if offset_y == -smallest else offset_x)
            e_y = center_y + (offset_y if offset_x == -smallest else 0)

            # Append the arc trace, centered around (center_x, center_y)
            self.common_form.append(
                CFSymmetricalArcTrace(
                    self.unit,
                    center_x + offset_x,  # Adjusted center offset
                    center_y + offset_y,  # Adjusted center offset
                    s_x,
                    s_y,
                    e_x,
                    e_y,
                    arc_len
                )
            )
