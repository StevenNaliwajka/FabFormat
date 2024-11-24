from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_circle import CFCircle
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_filled_symmetrical_arc import CFFilledSymmetricalArc
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent
from math import sqrt


class ObroundAperture(ApertureParent):
    def __init__(self, ap_number, center_x, center_y, x_size, y_size, unit, inside_hole_diam=None):
        # See Page 54:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # .../Gerber/GerberApertures/Apertures/Photos_Gerber2CF/Obround.png

        super().__init__(unit)
        self.aperture_type = "o"
        self.aperture_number = ap_number
        self.center_pt = (center_x, center_y)

        # To common form.
        self.to_common_form(x_size, y_size, inside_hole_diam)

    def to_common_form(self, x_size, y_size, inside_hole_diam=None):
        if inside_hole_diam:
            self.complex_obround_to_cf(x_size, y_size, inside_hole_diam)
        else:
            self.obround_to_cf(x_size, y_size)

    def obround_to_cf(self, x_size, y_size):
        if x_size == y_size:
            # If X size is equal to Y size, it's a circle.
            self.common_form.append(CFCircle(self.unit, self.center_pt, x_size / 2))
        else:
            # else createe obround
            self.create_obround(x_size, y_size)

    def complex_obround_to_cf(self, x_size, y_size, inside_hole_diam):
        if x_size == y_size:
            # if X size is equal to Y size, its a circle.
            self.common_form.append(CFCircle(self.unit, self.center_pt, x_size / 2, inside_hole_diam))
        else:
            # else create complex obround
            self.create_complex_obround(x_size, y_size, inside_hole_diam)

    def create_obround(self, x_size, y_size):
        # Determine the smallest.
        smallest = min(x_size, y_size)
        if smallest == x_size:
            # Smallest length is horizontal side.
            # Simple form create Rectangle #1
            self.rectangle_to_cf(self.center_pt, x_size, y_size - x_size)
        else:
            # Smallest length is vert side.
            # Simple form create Rectangle #1
            self.rectangle_to_cf(self.center_pt, x_size - y_size, y_size)
        # Simple form create ARCS, #2,3
        self.create_end_arcs(x_size, y_size)

    def create_complex_obround(self, x_size, y_size, inside_hole_diam):
        # Complex Obround: #1,2,3,4,5
        self.create_corner_arcs_and_inside_circle(self.center_pt, x_size, y_size, inside_hole_diam)

        smallest = min(x_size, y_size)
        if smallest == x_size:
            # X axis is smallest
            # Create RECT 6
            center_pt = (self.center_pt[0], self.center_pt[1] + (y_size / 4))
            rect_len_x = x_size
            rect_len_y = (y_size / 2) - x_size
            self.rectangle_to_cf(center_pt, rect_len_x, rect_len_y)

            # Create RECT 7
            center_pt = (self.center_pt[0], self.center_pt[1] - (y_size / 4))
            self.rectangle_to_cf(center_pt, rect_len_x, rect_len_y)

            # Create ARCS # 8,9
            self.create_end_arcs(x_size, y_size)
        else:
            # Y axis is smallest
            # Create RECT 6
            center_pt = (self.center_pt[0] - (x_size / 4), self.center_pt[1] - (y_size / 4))
            rect_len_x = (x_size / 2) - y_size
            rect_len_y = y_size
            self.rectangle_to_cf(center_pt, rect_len_x, rect_len_y)

            # Create RECT 7
            center_pt = (self.center_pt[0] + (x_size / 4), self.center_pt[1])
            self.rectangle_to_cf(center_pt, rect_len_x, rect_len_y)

            # Create ARCS # 8,9
            self.create_end_arcs(x_size, y_size)

    def create_end_arcs(self, x_size, y_size):

        smallest = min(x_size, y_size)
        if smallest == x_size:
            # Smallest length is horizontal side.

            # Solve distance from arc to center.
            dist_center = y_size / 2

            # FIRST ARC
            center_pt = (self.center_pt[0], self.center_pt[1] + dist_center)
            start_pt = (self.center_pt[0] - (x_size / 2), self.center_pt[1] + dist_center)
            end_pt = (self.center_pt[0] + (x_size / 2), self.center_pt[1] + dist_center)
            radius = x_size / 2
            self.common_form.append(CFFilledSymmetricalArc(self.unit, center_pt, start_pt, end_pt, radius))

            center_pt = (self.center_pt[0], self.center_pt[1] - dist_center)

            start_pt = (self.center_pt[0] + (x_size / 2), self.center_pt[1] - dist_center)
            end_pt = (self.center_pt[0] - (x_size / 2),self.center_pt[1] - dist_center)
            # Simple form create arc #3
            self.common_form.append(CFFilledSymmetricalArc(self.unit, center_pt, start_pt, end_pt, radius))

        else:
            # Smallest length is vertical side.

            # Solve distance from arc to center.
            dist_center = x_size / 2

            # FIRST ARC
            center_pt = (self.center_pt[0] - dist_center, self.center_pt[1])
            start_pt = (self.center_pt[0] - dist_center, self.center_pt[1] - (y_size / 2))
            end_pt = (self.center_pt[0] - dist_center, self.center_pt[1] + (y_size / 2))
            radius = y_size / 2
            self.common_form.append(CFFilledSymmetricalArc(self.unit, center_pt, start_pt, end_pt, radius))

            # SECOND ARC
            center_pt = (self.center_pt[0] + dist_center, self.center_pt[1])
            start_pt = (self.center_pt[0] + dist_center, self.center_pt[1] + (y_size / 2))
            end_pt = (self.center_pt[0] + dist_center, self.center_pt[1] - (y_size / 2))
            self.common_form.append(CFFilledSymmetricalArc(self.unit, center_pt, start_pt, end_pt, radius))
