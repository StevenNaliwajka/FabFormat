from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class ThermalAPMacro(APMacroParent):
    def __init__(self, center_x, center_y, outer_diameter, inner_diameter, gap, rotation=0):
        super().__init__()
        self.code = 7
        self.center_x = center_x
        self.center_y = center_y
        self.outer_diameter = outer_diameter
        self.inner_diameter = inner_diameter
        self.gap = gap
        self.rotation = rotation  # IN DEGREES CC
        self.common_form = []

        self.to_common_form()

    def to_common_form(self):
        pass
