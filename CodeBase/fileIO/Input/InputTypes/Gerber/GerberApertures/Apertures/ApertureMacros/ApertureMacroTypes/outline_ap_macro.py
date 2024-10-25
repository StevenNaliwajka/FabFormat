from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class OutlineAPMacro(APMacroParent):
    def __init__(self, exposure, num_vertices, start_x, start_y, point_list, rotation=0):
        super().__init__()
        self.code = 4
        self.exposure = exposure
        self.num_vertices = num_vertices
        self.start_x = start_x
        self.start_y = start_y
        self.point_list = point_list
        self.rotation = rotation  # IN DEGREES CC
        self.common_form = []

        self.to_common_form()

    def to_common_form(self):
        pass
