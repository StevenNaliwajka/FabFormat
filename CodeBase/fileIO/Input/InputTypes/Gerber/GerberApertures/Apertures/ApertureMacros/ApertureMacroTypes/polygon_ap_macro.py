from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class PolygonAPMacro(APMacroParent):
    def __init__(self, exposure, num_vertices, center_x, center_y, diameter, unit, rotation=0):
        # See Page 66:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy

        super().__init__(unit)
        self.code = 5
        self.exposure = exposure
        # Rotation in DEG CC
        self.to_common_form(num_vertices, (center_x, center_y), diameter, rotation)

    def to_common_form(self, num_vertices, center_pt, diameter, rotation):
        # In this form it's easier to handle the shape definition then handle rotation.
        coordinate_list = []

        # First Point
        new_pt = (center_pt[0] + (diameter / 2), center_pt[1])
        coordinate_list.append(new_pt)

        vertices_degree = 360 / num_vertices

        for _ in num_vertices:
            new_pt = self.rotate_point_around_origin_cc(new_pt, vertices_degree)
            coordinate_list.append(new_pt)

        if rotation is not 0:
            self._rotate_list(coordinate_list, rotation)

        self._am_create_polygon_cf(coordinate_list)
