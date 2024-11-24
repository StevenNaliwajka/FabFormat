from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class OutlineAPMacro(APMacroParent):
    def __init__(self, exposure, num_vertices, coordinate_list, unit, rotation=0):
        # See Page 64:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy
        super().__init__(unit)
        self.code = 4
        self.exposure = exposure
        # Rotation in DEG CC
        self.to_common_form(num_vertices, coordinate_list, rotation)

    def to_common_form(self, num_vertices, coordinate_list, rotation):
        if rotation is not 0:
            # Handle Rotation.
            # Num Vertices + 1 Because Start point is not included in count.
            self._rotate_list(coordinate_list, rotation)


        # Create Polygon OBJ
        self._am_create_polygon_cf(coordinate_list)
