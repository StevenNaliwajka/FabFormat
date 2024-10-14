from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent


class PolygonAperture(ApertureParent):
    def __init__(self, ap_number, outer_diameter, num_vertices, rotation, inside_hole_diam=None):
        super().__init__()
        self.aperture_type = "c"
        self.aperture_number = ap_number
        self.outer_diameter = outer_diameter
        self.num_vertices = num_vertices
        self.rotation = rotation
        self.inner_hole_diameter = inside_hole_diam
