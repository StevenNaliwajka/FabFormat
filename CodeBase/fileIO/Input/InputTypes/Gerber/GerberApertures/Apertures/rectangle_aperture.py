from math import sqrt

from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent


class RectangleAperture(ApertureParent):
    def __init__(self, ap_number, center_x, center_y, x_size, y_size, unit, inside_hole_diam=None):
        # See Page 53:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # .../Gerber/GerberApertures/Apertures/Photos_Gerber2CF/Rectangle.png

        super().__init__(unit)
        self.aperture_type = "r"
        self.aperture_number = ap_number
        self.x_size = x_size
        self.y_size = y_size
        self.inner_hole_diameter = inside_hole_diam

        # To common form.
        self.to_common_form((center_x, center_y), x_size, y_size, inside_hole_diam)

    def to_common_form(self, center_pt, x_size, y_size, inside_hole_diam):
        if inside_hole_diam:
            # Starts Creation of Complex Form
            self.complex_rectangle_to_cf(center_pt, x_size, y_size, inside_hole_diam)
        else:
            # Creats Simple form Polygon #1
            self.rectangle_to_cf(center_pt, x_size, y_size)

    def complex_rectangle_to_cf(self, center_pt, x_size, y_size, inside_hole_diam):
        # Complex Rectangle: #1,2,3,4,5
        self.create_corner_arcs_and_inside_circle(center_pt, x_size, y_size, inside_hole_diam)

        smallest = min(x_size, y_size)
        if smallest == x_size:
            # X axis is smallest
            # Create RECT 6
            rect_center_pt = (center_pt[0], center_pt[1] + (y_size+x_size)/4)
            rect_len_x = x_size
            rect_len_y = (y_size / 2) - (x_size/2)
            self.rectangle_to_cf(rect_center_pt, rect_len_x, rect_len_y)

            # Create RECT 7
            rect_center_pt = (center_pt[0], center_pt[1] - (y_size+x_size)/4)
            self.rectangle_to_cf(rect_center_pt, rect_len_x, rect_len_y)

        else:
            # Y axis is smallest
            # Create RECT 6
            rect_center_pt = (center_pt[0] + (y_size + x_size) / 4, center_pt[1])
            rect_len_x = (x_size / 2) - (y_size/2)
            rect_len_y = y_size
            self.rectangle_to_cf(rect_center_pt, rect_len_x, rect_len_y)

            # Create RECT 7
            rect_center_pt = (center_pt[0] - (y_size + x_size) / 4, center_pt[1])
            self.rectangle_to_cf(rect_center_pt, rect_len_x, rect_len_y)