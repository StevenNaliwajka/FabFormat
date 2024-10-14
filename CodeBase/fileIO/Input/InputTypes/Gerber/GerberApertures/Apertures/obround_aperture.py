from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent


class ObroundAperture(ApertureParent):
    def __init__(self, ap_number, x_size, y_size, inside_hole_diam=None):
        super().__init__()
        self.aperture_type = "o"
        self.aperture_number = ap_number
        self.x_size = x_size
        self.y_size = y_size
        self.inner_hole_diameter = inside_hole_diam
