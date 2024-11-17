from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_symmetrical_arc_trace import CFSymmetricalArcTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent
from math import sqrt


class ObroundAperture(ApertureParent):
    def __init__(self, ap_number, x_size, y_size, inside_hole_diam=None):
        # See Page 54:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # .../Gerber/GerberApertures/Apertures/Photos_Gerber2CF/Obround.png

        super().__init__()
        self.aperture_type = "o"
        self.aperture_number = ap_number
        self.to_common_form(x_size, y_size, inside_hole_diam)

    def to_common_form(self, x_size, y_size, inside_hole_diam=None):
        if inside_hole_diam:
            self.complex_obround_to_cf(x_size, y_size, inside_hole_diam)
        else:
            self.obround_to_cf(x_size, y_size)

    def obround_to_cf(self, x_size, y_size):
        if x_size == y_size:
            self.common_form.append(CFCircleTrace(0, 0, x_size / 2))
        else:
            self.create_obround(x_size, y_size)

    def complex_obround_to_cf(self, x_size, y_size, inside_hole_diam):
        if x_size == y_size:
            self.common_form.append(CFCircleTrace(0, 0, x_size / 2, inside_hole_diam))
        else:
            self.create_complex_obround(x_size, y_size, inside_hole_diam)

    def create_obround(self, x_size, y_size):
        smallest = min(x_size, y_size)
        if smallest == x_size:
            self.create_rectangle_and_arcs(x_size, y_size - x_size, x_size / 2, (y_size - x_size) / 2)
        else:
            self.create_rectangle_and_arcs(x_size - y_size, y_size, y_size / 2, (x_size - y_size) / 2)

    def create_complex_obround(self, x_size, y_size, inside_hole_diam):
        smallest = min(x_size, y_size)
        self.common_form.append(CFCircleTrace(0, 0, smallest, inside_hole_diam))
        arc_len = sqrt((smallest ** 2) + (smallest ** 2)) - smallest
        self.create_corner_arcs(smallest, arc_len)
        if smallest == x_size:
            self.create_rectangle_and_arcs(x_size, y_size - x_size, x_size / 2, (y_size - x_size) / 2)
        else:
            self.create_rectangle_and_arcs(x_size - y_size, y_size, y_size / 2, (x_size - y_size) / 2)

    def create_rectangle_and_arcs(self, rect_x, rect_y, sagitta, dist_center):
        self.rectangle_to_cf(0, 0, rect_x, rect_y)
        self.common_form.append(
            CFSymmetricalArcTrace(0, dist_center, -sagitta, dist_center, sagitta, dist_center, sagitta))
        self.common_form.append(
            CFSymmetricalArcTrace(0, -dist_center, sagitta, -dist_center, -sagitta, -dist_center, sagitta))

    def create_corner_arcs(self, size, arc_len):
        corner_offsets = [(-size, -size), (-size, size), (size, size), (size, -size)]
        for offset_x, offset_y in corner_offsets:
            s_x, s_y = offset_x, 0 if offset_y else -size
            e_x, e_y = 0 if offset_x else -size, offset_y
            self.common_form.append(CFSymmetricalArcTrace(offset_x, offset_y, s_x, s_y, e_x, e_y, arc_len))