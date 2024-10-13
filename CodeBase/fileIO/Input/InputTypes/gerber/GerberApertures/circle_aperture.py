from CodeBase.fileIO.Input.InputTypes.gerber.GerberApertures.aperture_parent import ApertureParent


class CircleAperture(ApertureParent):
    def __init__(self, ap_number, diameter, in_hole_diam):
        self.aperture_type = "C"
        self.aperture_number = ap_number
        self.diameter = diameter
        self.inner_hole_diameter = in_hole_diam

        