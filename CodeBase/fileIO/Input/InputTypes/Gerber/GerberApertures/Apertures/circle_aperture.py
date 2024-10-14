from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent


class CircleAperture(ApertureParent):
    def __init__(self, ap_number, diameter, inside_hole_diam=None):
        super().__init__()
        self.aperture_type = "c"
        self.aperture_number = ap_number
        self.diameter = diameter
        self.inner_hole_diameter = inside_hole_diam
