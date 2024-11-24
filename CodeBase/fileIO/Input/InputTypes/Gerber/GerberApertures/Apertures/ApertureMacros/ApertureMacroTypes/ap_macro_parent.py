import math
from abc import abstractmethod

from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFComposites.cf_polygon import CFPolygon
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFPrimitives.cf_linear_prim import CFLinearPrim


class APMacroParent:
    def __init__(self, unit):
        self.code = None
        self.exposure = None
        self.common_form = []
        self.unit = unit

    @abstractmethod
    def to_common_form(self, *args, **kwargs):
        pass

    def rotate_point_around_origin_cc(self, pt, cc_degrees):
        # Formula for CC (Counter-Clockwise) Degree Rotation around origin
        # X' = x * cos(θ) - y * sin(θ)
        # Y' = x * sin(θ) + y * cos(θ)

        # Convert angle from degrees to radians
        angle_radians = math.radians(cc_degrees)

        # Apply the rotation
        rotated_x = pt[0] * math.cos(angle_radians) - pt[1] * math.sin(angle_radians)
        rotated_y = pt[0] * math.sin(angle_radians) + pt[1] * math.cos(angle_radians)

        return rotated_x, rotated_y

    def am_create_rectangle_cf(self, width, height, center_pt, rotation):

        coordinate_list = []
        # Convert to polygon. Solve for vertices.
        # Bottom left
        new_x_coordinate = center_pt[0] - (width / 2)
        new_y_coordinate = center_pt[1] - (height / 2)
        coordinate_list.append((new_x_coordinate, new_y_coordinate))
        # Top left
        new_y_coordinate = new_y_coordinate + height
        coordinate_list.append((new_x_coordinate, new_y_coordinate))
        # Top right
        new_x_coordinate = new_x_coordinate + height
        coordinate_list.append((new_x_coordinate, new_y_coordinate))
        # Bottom Right
        new_y_coordinate = new_y_coordinate - height
        coordinate_list.append((new_x_coordinate, new_y_coordinate))
        # Bottom Left again.
        new_x_coordinate = new_x_coordinate - width
        coordinate_list.append((new_x_coordinate, new_y_coordinate))

        if rotation:
            # Itterates through each point pair and rotates each.
            self._rotate_list(coordinate_list, rotation)

        self._am_create_polygon_cf(coordinate_list)
    def _am_create_polygon_cf(self, coordinate_list):
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

    def _rotate_list(self, coordinate_list, rotation):
        for index, pt in enumerate(coordinate_list):
            new_point = self.rotate_point_around_origin_cc(pt, rotation)
            coordinate_list[index] = new_point
