from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class PolygonAPMacro(APMacroParent):
    def __init__(self, exposure, num_vertices, center_x, center_y, diameter, rotation=0):
        super().__init__()
        self.code = 5
        self.exposure = exposure
        self.num_vertices = num_vertices
        self.center_x = center_x
        self.center_y = center_y
        self.diameter = diameter
        self.rotation = rotation  # IN DEGREES CC
        self.common_form = []

        self.to_common_form()

    def to_common_form(self):
        pass
