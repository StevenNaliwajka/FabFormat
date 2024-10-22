from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class CircleAPMacro(APMacroParent):
    def __init__(self, exposure, diameter, center_x, center_y, rotation=0):
        super().__init__()
        self.code = 1
        self.exposure = exposure
        self.diameter = diameter
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation  # IN DEGREES CC
