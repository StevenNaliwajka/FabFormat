from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.curves.cf_symmetrical_arc_trace import \
    CFSymmetricalArcTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent
from math import sqrt


class PolygonAperture(ApertureParent):
    def __init__(self, ap_number, outer_diameter, num_vertices, rotation, inside_hole_diam=None):
        # See Page 55:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy

        super().__init__()
        self.aperture_type = "c"
        self.aperture_number = ap_number
        self.outer_diameter = outer_diameter
        self.num_vertices = num_vertices
        self.rotation = rotation
        self.inner_hole_diameter = inside_hole_diam

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
                polygon_x_size = x_size
                polygon_y_size = y_size/2 - x_size
                center_y = (polygon_y_size/2) + (x_size/2)
                center_x = 0
                self.rectangle_to_cf(center_x, center_y, polygon_x_size, polygon_y_size)
                self.rectangle_to_cf(center_x, -center_y, polygon_x_size, polygon_y_size)


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
                polygon_x_size = x_size / 2 - y_size
                polygon_y_size = y_size
                center_y = 0
                center_x = (polygon_x_size / 2) + (y_size / 2)
                self.rectangle_to_cf(-center_x, center_y, polygon_x_size, polygon_y_size)
                self.rectangle_to_cf(center_x, center_y, polygon_x_size, polygon_y_size)
