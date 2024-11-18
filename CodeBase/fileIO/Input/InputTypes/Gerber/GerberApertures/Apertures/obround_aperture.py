from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_symmetrical_arc_trace import CFSymmetricalArcTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent
from math import sqrt


class ObroundAperture(ApertureParent):
    def __init__(self, ap_number, center_x, center_y, x_size, y_size, unit, inside_hole_diam=None):
        # See Page 54:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # .../Gerber/GerberApertures/Apertures/Photos_Gerber2CF/Obround.png

        super().__init__()
        self.aperture_type = "o"
        self.aperture_number = ap_number
        self.center_x = center_x
        self.center_y = center_y
        self.unit = unit

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
            self.common_form.append(CFCircleTrace(self.center_x, self.center_y, x_size / 2))
        else:
            # else createe obround
            self.create_obround(x_size, y_size)

    def complex_obround_to_cf(self, x_size, y_size, inside_hole_diam):
        if x_size == y_size:
            # if X size is equal to Y size, its a circle.
            self.common_form.append(CFCircleTrace(self.center_x, self.center_y, x_size / 2, inside_hole_diam))
        else:
            # else create complex obround
            self.create_complex_obround(x_size, y_size, inside_hole_diam)

    def create_obround(self, x_size, y_size):
        # Determine the smallest.
        smallest = min(x_size, y_size)
        if smallest == x_size:
            # Smallest length is horizontal side.
            # Simple form create Rectangle #1
            self.rectangle_to_cf(self.center_x, self.center_y, x_size, y_size - x_size)
        else:
            # Smallest length is vert side.
            # Simple form create Rectangle #1
            self.rectangle_to_cf(self.center_x, self.center_y, x_size - y_size, y_size)
        # Simple form create ARCS, #2,3
        self.create_end_arcs(x_size,y_size)

    def create_complex_obround(self, x_size, y_size, inside_hole_diam):
        # Complex Obround: #1,2,3,4,5
        self.create_corner_arcs_and_inside_circle(self.center_x, self.center_y, x_size, y_size, inside_hole_diam)

        smallest = min(x_size, y_size)
        if smallest == x_size:
            # X axis is smallest
            # Create RECT 6
            center_x = self.center_x
            center_y = self.center_y + (y_size/4)
            rect_len_x = x_size
            rect_len_y = (y_size/2)-x_size
            self.rectangle_to_cf(center_x, center_y, rect_len_x, rect_len_y)

            # Create RECT 7
            center_x = self.center_x
            center_y = self.center_y - (y_size/4)
            self.rectangle_to_cf(center_x, center_y, rect_len_x, rect_len_y)

            # Create ARCS # 8,9
            self.create_end_arcs(x_size,y_size)
        else:
            # Y axis is smallest
            # Create RECT 6
            center_x = self.center_x - (x_size / 4)
            center_y = self.center_y
            rect_len_x = (x_size / 2) - y_size
            rect_len_y = y_size
            self.rectangle_to_cf(center_x, center_y, rect_len_x, rect_len_y)

            # Create RECT 7
            center_x = self.center_x + (x_size / 4)
            center_y = self.center_y
            self.rectangle_to_cf(center_x, center_y, rect_len_x, rect_len_y)

            # Create ARCS # 8,9
            self.create_end_arcs(x_size, y_size)

    def create_end_arcs(self, x_size, y_size):

        smallest = min(x_size, y_size)
        if smallest == x_size:
            # Smallest length is horizontal side.

            # Solve distance from arc to center.
            dist_center = y_size / 2

            # FIRST ARC
            center_x = self.center_x
            center_y = self.center_y + dist_center
            start_x = self.center_x - (x_size / 2)
            start_y = self.center_y + dist_center
            end_x = self.center_x + (x_size / 2)
            end_y = self.center_y + dist_center
            radius = x_size / 2
            self.common_form.append(CFSymmetricalArcTrace(center_x, center_y, start_x, start_y, end_x, end_y, radius))

            center_x = self.center_x
            center_y = self.center_y - dist_center
            start_x = self.center_x + (x_size / 2)
            start_y = self.center_y - dist_center
            end_x = self.center_x - (x_size / 2)
            end_y = self.center_y - dist_center
            # Simple form create arc #3
            self.common_form.append(CFSymmetricalArcTrace(center_x, center_y, start_x, start_y, end_x, end_y, radius))

        else:
            # Smallest length is vertical side.

            # Solve distance from arc to center.
            dist_center = x_size / 2

            # FIRST ARC
            center_x = self.center_x - dist_center
            center_y = self.center_y
            start_x = self.center_x - dist_center
            start_y = self.center_y - (y_size / 2)
            end_x = self.center_x - dist_center
            end_y = self.center_y + (y_size / 2)
            radius = y_size / 2
            self.common_form.append(CFSymmetricalArcTrace(center_x, center_y, start_x, start_y, end_x, end_y, radius))

            # SECOND ARC
            center_x = self.center_x + dist_center
            center_y = self.center_y
            start_x = self.center_x + dist_center
            start_y = self.center_y + (y_size / 2)
            end_x = self.center_x + dist_center
            end_y = self.center_y - (y_size / 2)
            self.common_form.append(CFSymmetricalArcTrace(center_x, center_y, start_x, start_y, end_x, end_y, radius))
