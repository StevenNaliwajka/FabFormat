import math

from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_symmetrical_arc_trace import CFSymmetricalArcTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent
from math import sqrt


class ThermalAPMacro(APMacroParent):
    def __init__(self, center_x, center_y, outer_diameter, inner_diameter, gap, rotation=0):
        # See Page 67:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy

        super().__init__()
        self.code = 7
        self.exposure = 1

        self.to_common_form(center_x, center_y, outer_diameter, inner_diameter, gap, rotation)

    def to_common_form(self, center_x, center_y, outer_diameter, inner_diameter, gap, rotation):
        # Creates 4 Arc CF units.
        # Note that ARC only works Clockwise.

        # Used to find the 'arc true' center of the current arc.
        yoff = gap / 2
        xoff = gap / 2
        arc_center_offset = sqrt((yoff ^ 2) + (xoff ^ 2))
        # Calculates the radius from 'arc true' center to the outer edge of the ring
        arc_outer_radius = (outer_diameter / 2) - arc_center_offset
        # Calculates the radius from 'arc true' center to the inner edge of the ring
        arc_inner_radius = (inner_diameter / 2) - arc_center_offset

        # Calls create arc method 4 times for the 4 unique arcs.
        self.create_arc(center_x, center_y, xoff, yoff, arc_outer_radius, arc_inner_radius, "bottom left", rotation)
        self.create_arc(center_x, center_y, xoff, yoff, arc_outer_radius, arc_inner_radius, "top left", rotation)
        self.create_arc(center_x, center_y, xoff, yoff, arc_outer_radius, arc_inner_radius, "top right", rotation)
        self.create_arc(center_x, center_y, xoff, yoff, arc_outer_radius, arc_inner_radius, "bottom right", rotation)

    def create_arc(self, center_x, center_y, xoff, yoff, outer_radius, inner_radius, position, rotation):
        # Set arc center based on position
        arc_center_x = center_x + (xoff if "right" in position else -xoff)
        arc_center_y = center_y + (yoff if "top" in position else -yoff)

        # Determine outer and inner points based on position
        if "top" in position:
            outer_x, outer_y = (arc_center_x - outer_radius, arc_center_y) if "left" in position else (
                arc_center_x, arc_center_y + outer_radius)
        else:
            outer_x, outer_y = (arc_center_x + outer_radius, arc_center_y) if "right" in position else (
                arc_center_x, arc_center_y - outer_radius)

        # Create arc Will always be 90 Deg.
        self.handle_rotation_and_create_cf_arc(arc_center_x, arc_center_y, outer_x, outer_y, outer_radius, inner_radius,
                                               90, rotation)

    def handle_rotation_and_create_cf_arc(self, arc_center_x, arc_center_y, outer_x, outer_y, outer_radius,
                                          inner_radius, degree_cw, rotation):
        end_x, end_y = self.rotate_point(outer_x, outer_y, arc_center_x, arc_center_y, degree_cw)

        if rotation is not 0:
            arc_center_x, arc_center_y = self.rotate_point_around_origin_cc(arc_center_x, arc_center_y, rotation)
            outer_x, outer_y = self.rotate_point_around_origin_cc(outer_x, outer_y, rotation)

        new_cf_instruction = CFSymmetricalArcTrace(arc_center_x, arc_center_y, outer_x, outer_y, end_x, end_y,
                                                   outer_radius, inner_radius)
        self.common_form.append(new_cf_instruction)

    def rotate_point(self, x, y, cx, cy, angle_degrees):
        # Convert the angle from degrees to radians
        angle_radians = math.radians(angle_degrees)

        # Step 1: Translate point X to the origin based on center C
        x_translated = x - cx
        y_translated = y - cy

        # Step 2: Apply the rotation formula
        x_rotated = x_translated * math.cos(angle_radians) + y_translated * math.sin(angle_radians)
        y_rotated = -x_translated * math.sin(angle_radians) + y_translated * math.cos(angle_radians)

        # Step 3: Translate the rotated point back to the original position
        x_final = x_rotated + cx
        y_final = y_rotated + cy

        return x_final, y_final
