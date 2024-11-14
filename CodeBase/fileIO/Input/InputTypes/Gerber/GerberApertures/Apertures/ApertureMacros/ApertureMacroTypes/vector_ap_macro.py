
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class VectorAPMacro(APMacroParent):
    def __init__(self, exposure, width, start_x, start_y, end_x, end_y, rotation=0):
        # See Page 62:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy

        super().__init__()
        self.code = 20
        self.exposure = exposure

        self.to_common_form(width, start_x, start_y, end_x, end_y, rotation)

    def to_common_form(self, width, start_x, start_y, end_x, end_y, rotation):
        coordinate_list = []
        # Convert to polygon. Solve for vertices.
        # Bottom left
        new_x_coordinate = start_x
        new_y_coordinate = start_y - (width/2)
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        # Top left
        new_y_coordinate = start_y + width
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        # Top right
        new_x_coordinate = end_x
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        # Bottom Right
        new_y_coordinate = start_y - width
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        # Bottom left again. To return to OG
        new_x_coordinate = start_x
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        if rotation is not 0:
            for point in range(5):
                # Iterates through each point pair and rotates each.
                current_x = coordinate_list[(point - 1) * 2]
                current_y = coordinate_list[((point - 1) * 2) + 1]
                new_x, new_y = self.rotate_point_around_origin_cc(current_x, current_y, rotation)
                # Set new point
                coordinate_list[(point - 1) * 2] = new_x
                coordinate_list[((point - 1) * 2) + 1] = new_y

        # Create Polygon OBJ
        new_common_form = CFPolygonTrace(coordinate_list)
        self.common_form.append(new_common_form)
