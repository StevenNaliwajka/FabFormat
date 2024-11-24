from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class VectorAPMacro(APMacroParent):
    def __init__(self, exposure, width, start_x, start_y, end_x, end_y, unit, rotation=0):
        # See Page 62:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy

        super().__init__(unit)
        self.code = 20
        self.exposure = exposure

        self.to_common_form(width, start_x, start_y, end_x, end_y, rotation)

    def to_common_form(self, width, start_x, start_y, end_x, end_y, rotation):
        coordinate_list = []
        # Convert to polygon. Solve for vertices.
        # Bottom left
        new_coordinate = (start_x, start_y - (width/2))
        coordinate_list.append(new_coordinate)

        # Top left
        new_coordinate = (start_x, start_y + width)
        coordinate_list.append(new_coordinate)

        # Top right
        new_coordinate = (end_x, start_y + width)
        coordinate_list.append(new_coordinate)

        # Bottom Right
        new_coordinate = (end_x, start_y - width)
        coordinate_list.append(new_coordinate)

        # Bottom left again. To return to OG
        new_coordinate = (start_x, start_y - width)
        coordinate_list.append(new_coordinate)

        if rotation is not 0:
            self._rotate_list(coordinate_list, rotation)

        # Create Polygon OBJ
        self._am_create_polygon_cf(coordinate_list)
