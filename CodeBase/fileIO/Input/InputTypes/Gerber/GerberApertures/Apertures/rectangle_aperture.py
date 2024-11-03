from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent


class RectangleAperture(ApertureParent):
    def __init__(self, ap_number, x_size, y_size, inside_hole_diam=None):
        # See Page 53:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # .../Gerber/GerberApertures/Apertures/Photos_Gerber2CF/Rectangle.png

        super().__init__()
        self.aperture_type = "r"
        self.aperture_number = ap_number
        self.x_size = x_size
        self.y_size = y_size
        self.inner_hole_diameter = inside_hole_diam
        self.to_common_form(x_size, y_size, inside_hole_diam)

    def to_common_form(self, x_size, y_size, inside_hole_diam):
        if inside_hole_diam:
            self.complex_rectangle_to_cf(x_size, y_size, inside_hole_diam)
        else:
            self.rectangle_to_cf(x_size, y_size)
