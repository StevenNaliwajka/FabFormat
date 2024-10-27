from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.curves.cf_symmetrical_arc_trace import \
    CFSymmetricalArcTrace
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

    def to_common_form(self, x_size, y_size, inside_hole_diam):
        if inside_hole_diam:
            self.complex_obround_to_cf(x_size, y_size, inside_hole_diam)
        else:
            self.obround_to_cf(x_size, y_size)

    def obround_to_cf(self, x_size, y_size):
        if x_size == y_size:
            # It's a circle.
            self.common_form.append(CFCircleTrace(0, 0, x_size / 2))
        else:
            self.create_obround_common_form(x_size, y_size)

    def create_obround_common_form(self, x_size, y_size):
        smallest = min(x_size, y_size)
        sagitta = smallest / 2
        distance_to_center_arc_from_center = abs((max(x_size, y_size) / 2) - sagitta)

        if smallest == x_size:
            self.create_rectangle_and_arcs(0, distance_to_center_arc_from_center, x_size, y_size, sagitta, "vertical")
        else:
            self.create_rectangle_and_arcs(distance_to_center_arc_from_center, 0, x_size, y_size, sagitta, "horizontal")

    def complex_obround_to_cf(self, x_size, y_size, inside_hole_diam):
        if x_size == y_size:
            self.common_form.append(CFCircleTrace(0, 0, x_size / 2, inside_hole_diam))
        else:
            smallest = min(x_size, y_size)
            circle_diameter = smallest
            self.common_form.append(CFCircleTrace(0, 0, circle_diameter, inside_hole_diam))
            arc_len = (circle_diameter * (2 ** 0.5)) - circle_diameter
            self.create_four_arcs(circle_diameter, arc_len)

            if smallest == x_size:
                self.create_polygons_for_complex(x_size, y_size, inside_hole_diam, offset_axis="y")
            else:
                self.create_polygons_for_complex(y_size, x_size, inside_hole_diam, offset_axis="x")

    def create_rectangle_and_arcs(self, center_x, center_y, x_size, y_size, sagitta, orientation):
        # Create rectangle
        polygon_x, polygon_y = (x_size, y_size - x_size) if orientation == "vertical" else (x_size - y_size, y_size)
        self.rectangle_to_cf(0, 0, polygon_x, polygon_y)

        # Create two CF symmetrical arcs
        for sign in (-1, 1):
            arc_center = (center_x * sign, center_y * sign) if orientation == "horizontal" else (
            center_x * sign, center_y)
            self.common_form.append(
                CFSymmetricalArcTrace(*arc_center, arc_center[0] - sagitta, arc_center[1], arc_center[0] + sagitta,
                                      arc_center[1], sagitta))

    def create_four_arcs(self, diameter, arc_len):
        for cx, cy in [(-diameter, -diameter), (-diameter, diameter), (diameter, diameter), (diameter, -diameter)]:
            self.common_form.append(
                CFSymmetricalArcTrace(cx, cy, cx + (cx // abs(cx)) * diameter, cy, cx, cy + (cy // abs(cy)) * diameter,
                                      arc_len))

    def create_polygons_for_complex(self, x_size, y_size, inside_hole_diam, offset_axis="y"):
        center_offset = ((max(x_size, y_size) / 2) - (min(x_size, y_size) - 2)) / 2 + (min(x_size, y_size) / 2)
        for sign in (-1, 1):
            if offset_axis == "y":
                self.rectangle_to_cf(0, center_offset * sign, x_size, y_size)
            else:
                self.rectangle_to_cf(center_offset * sign, 0, x_size, y_size)

    # Above code was simplified from below code I wrote. Hopefully it works
    '''
    def to_common_form(self, x_size, y_size, inside_hole_diam):
        if inside_hole_diam:
            self.complex_obround_to_cf(x_size, y_size, inside_hole_diam)
        else:
            self.obround_to_cf(x_size, y_size)

    def obround_to_cf(self, x_size, y_size):
        if x_size == y_size:
            # its a circle lol.
            new_common_form = CFCircleTrace(0,0, x_size/2)
            self.common_form.append(new_common_form)

        # Creates 2 CF arcs and 1 CF polygon.
        # See picture referenced in constructor.

        else:
            smallest = min(x_size, y_size)
            if smallest == x_size:
                # X IS SMALLEST
                sagitta = x_size/2
                distance_to_center_arc_from_center = (y_size/2)-sagitta
                # Create polygon
                polygon_x = x_size
                polygon_y = y_size-x_size
                self.rectangle_to_cf(0,0,polygon_x,polygon_y)
                # Create two CF symarcs
                # ARC 1
                c_x = 0
                c_y = distance_to_center_arc_from_center
                s_x = c_x-sagitta
                s_y = c_y
                e_x = c_x+sagitta
                e_y = c_y
                new_common_form = CFSymmetricalArcTrace(c_x,c_y,s_x,s_y,e_x,e_y,sagitta)
                self.common_form.append(new_common_form)
                # ARC 2
                c_x = 0
                c_y = -distance_to_center_arc_from_center
                s_x = c_x + sagitta
                s_y = c_y
                e_x = c_x - sagitta
                e_y = c_y
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, sagitta)
                self.common_form.append(new_common_form)

            elif smallest == y_size:
                # Y IS SMALLEST
                sagitta = y_size/2
                distance_to_center_arc_from_center = (x_size / 2) - sagitta
                # Create polygon
                polygon_x = x_size - y_size
                polygon_y = y_size
                self.rectangle_to_cf(0,0 polygon_x, polygon_y)
                # Create two CF symarcs
                # ARC 1
                c_x = -distance_to_center_arc_from_center
                c_y = 0
                s_x = c_x
                s_y = c_y - sagitta
                e_x = c_x
                e_y = c_y + sagitta
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, sagitta)
                self.common_form.append(new_common_form)
                # ARC 2
                c_x = distance_to_center_arc_from_center
                c_y = 0
                s_x = c_x
                s_y = c_y + sagitta
                e_x = c_x
                e_y = c_y - sagitta
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, sagitta)
                self.common_form.append(new_common_form)

    def complex_obround_to_cf(self, x_size, y_size, inside_hole_diam):
        if x_size == y_size:
            # its a circle lol.
            new_common_form = CFCircleTrace(0,0, x_size/2, inside_hole_diam)
            self.common_form.append()

        # Creates 1 CF circle, 4 CF arcs and 2 CF polygons.
        # See picture referenced in constructor.

        # Create CF Circle
        # Inner Diam from inside_hole_diam
        # Inner Diam =  which ever is smallest (x_size or y_size)

        else:
            smallest = min(x_size, y_size)
            if smallest == x_size:
                # Create CF circle
                new_common_form = CFCircleTrace(0, 0, x_size, inside_hole_diam)
                self.common_form.append(new_common_form)

                # Create 4 CF arcs
                rectangle_corner_len = sqrt((smallest^2) + (smallest^2))
                arc_len = rectangle_corner_len - smallest


                #BL ARC
                c_x = 0-smallest
                c_y = 0-smallest
                s_x = 0
                s_y = 0-smallest
                e_x = 0-smallest
                e_y = 0
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, arc_len)
                self.common_form.append(new_common_form)
                # TL ARC
                c_x = 0 - smallest
                c_y = 0 + smallest
                s_x = 0 - smallest
                s_y = 0
                e_x = 0
                e_y = 0 + smallest
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, arc_len)
                self.common_form.append(new_common_form)
                # TR ARC
                c_x = 0 + smallest
                c_y = 0 + smallest
                s_x = 0
                s_y = 0 + smallest
                e_x = 0 + smallest
                e_y = 0
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, arc_len)
                self.common_form.append(new_common_form)
                # BL ARC
                c_x = 0 + smallest
                c_y = 0 - smallest
                s_x = 0 + smallest
                s_y = 0
                e_x = 0
                e_y = 0 - smallest
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, arc_len)
                self.common_form.append(new_common_form)

                # Create two Polygons
                # Poly1
                center_y = (((y_size/2)-(x_size-2))/2) + (x_size/2)
                center_x = 0
                self.rectangle_to_cf(center_x, center_y, x_size, y_size)
                self.rectangle_to_cf(center_x, -center_y, x_size, y_size)

            else:
                # Create CF circle
                new_common_form = CFCircleTrace(0, 0, y_size, inside_hole_diam)
                self.common_form.append(new_common_form)

                # Create 4 CF arcs
                rectangle_corner_len = sqrt((smallest ^ 2) + (smallest ^ 2))
                arc_len = rectangle_corner_len - smallest

                # BL ARC
                c_x = 0 - smallest
                c_y = 0 - smallest
                s_x = 0
                s_y = 0 - smallest
                e_x = 0 - smallest
                e_y = 0
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, arc_len)
                self.common_form.append(new_common_form)
                # TL ARC
                c_x = 0 - smallest
                c_y = 0 + smallest
                s_x = 0 - smallest
                s_y = 0
                e_x = 0
                e_y = 0 + smallest
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, arc_len)
                self.common_form.append(new_common_form)
                # TR ARC
                c_x = 0 + smallest
                c_y = 0 + smallest
                s_x = 0
                s_y = 0 + smallest
                e_x = 0 + smallest
                e_y = 0
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, arc_len)
                self.common_form.append(new_common_form)
                # BL ARC
                c_x = 0 + smallest
                c_y = 0 - smallest
                s_x = 0 + smallest
                s_y = 0
                e_x = 0
                e_y = 0 - smallest
                new_common_form = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, arc_len)
                self.common_form.append(new_common_form)

                # Create two Polygons
                # Poly1
                center_y = 0
                center_x = (((x_size / 2) - (y_size - 2)) / 2) + (y_size / 2)
                self.rectangle_to_cf(-center_x, center_y, x_size, y_size)
                self.rectangle_to_cf(center_x, center_y, x_size, y_size)

    '''