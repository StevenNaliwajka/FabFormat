from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class CenterAPMacro(APMacroParent):
    def __init__(self, exposure, width, height, center_x, center_y, rotation=0):
        super().__init__()
        self.code = 21
        self.exposure = exposure
        # Rotation in DEG CC
        self.to_common_form(width, height, center_x, center_y, rotation)

    def to_common_form(self, width, height, center_x, center_y, rotation):

        coordinate_list = []
        # Convert to polygon. Solve for vertices.
        # Bottom left
        new_x_coordinate = center_x - (width / 2)
        new_y_coordinate = center_y - (height / 2)
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)
        # Top left
        new_y_coordinate = new_y_coordinate + height
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)
        # Top right
        new_x_coordinate = new_x_coordinate + height
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)
        # Bottom Right
        new_y_coordinate = new_y_coordinate - height
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)
        # Bottom Left again.
        new_x_coordinate = new_x_coordinate - width
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        if rotation is not 0:
            for point in range(5):
                # Itterates through each point pair and rotates each.
                current_x = coordinate_list[(point - 1) * 2]
                current_y = coordinate_list[((point - 1) * 2) + 1]
                new_x, new_y = self.rotate_point_around_origin_cc(current_x, current_y, rotation)
                # Set new point
                coordinate_list[(point - 1) * 2] = new_x
                coordinate_list[((point - 1) * 2) + 1] = new_y
        # Create Polygon OBJ
        new_common_form = CFPolygonTrace(coordinate_list)
        self.common_form.append(new_common_form)
