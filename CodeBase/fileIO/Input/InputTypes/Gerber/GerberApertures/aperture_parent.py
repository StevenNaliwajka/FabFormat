from abc import abstractmethod
from math import sqrt

from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFComposites.cf_polygon import CFPolygon
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFPrimitives.cf_linear_prim import CFLinearPrim
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_circle import CFCircle
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_filled_symmetrical_arc import CFFilledSymmetricalArc


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

    def rectangle_to_cf(self, center_pt, x_size, y_size):
        # Creates 1 CF polygon: EZ
        point_list = []
        # BL: BOTTOM LEFT
        # BR: BOTTOM RIGHT
        # TL: TOP LEFT
        # TR: TOP RIGHT
        # BL
        current_pt = (center_pt[0] - (x_size / 2), center_pt[1] - (y_size / 2))
        point_list.append(current_pt)
        # TL
        current_pt = (center_pt[0] - (x_size / 2), center_pt[1] + y_size)
        point_list.append(current_pt)
        # TR
        current_pt = (center_pt[0] + x_size, center_pt[1] + y_size)
        point_list.append(current_pt)
        # BR
        current_pt = (center_pt[0] + x_size, center_pt[1] - y_size)
        point_list.append(current_pt)
        # BLx2
        current_pt = (center_pt[0] - x_size, center_pt[1] - y_size)
        point_list.append(current_pt)

        self._a_create_polygon_cf(point_list)

    def create_corner_arcs_and_inside_circle(self, center_pt, x_size, y_size, inside_hole_diam):
        # Used by Complex Rectangle and Complex Obround
        # Complex Rectangle: #1,2,3,4,5
        # Complex Obround: #1,2,3,4,5

        # Determine smallest axis
        smallest = min(x_size, y_size)
        # In complex variation, Create Circle #1
        self.common_form.append(CFCircle(self.unit, center_pt, smallest, inside_hole_diam))

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
            s_x = center_pt[0] + (offset_x if offset_y == -smallest else 0)
            s_y = center_pt[1] + (0 if offset_x == -smallest else offset_y)
            e_x = center_pt[0] + (0 if offset_y == -smallest else offset_x)
            e_y = center_pt[1] + (offset_y if offset_x == -smallest else 0)

            # Append the arc trace, centered around (center_x, center_y)
            self.common_form.append(
                CFFilledSymmetricalArc(
                    self.unit,
                    (center_pt[0] + offset_x, center_pt[1] + offset_y),  # Adjusted center offset
                    (s_x, s_y),
                    (e_x, e_y),
                    arc_len
                )
            )

    def _a_create_polygon_cf(self, coordinate_list):
        # Create Polygon OBJ

        # Creates new CF LINEAR obj, adds it to the correct list + layer
        linear_prim_list = []
        i = 0
        j = 1
        while j <= len(coordinate_list):
            linear_prim_list.append(CFLinearPrim(self.unit, coordinate_list[i], coordinate_list[j]))
            i += 1
            j += 1

        # create polygon
        self.common_form.append(CFPolygon(self.unit, coordinate_list))
