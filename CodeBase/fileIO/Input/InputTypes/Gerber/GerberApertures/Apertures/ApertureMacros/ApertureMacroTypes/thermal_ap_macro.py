from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_arc_trace import CFArcTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent
from math import sqrt


class ThermalAPMacro(APMacroParent):
    def __init__(self, center_x, center_y, outer_diameter, inner_diameter, gap, rotation=0):
        super().__init__()
        self.code = 7
        self.exposure = 1

        self.to_common_form(center_x, center_y, outer_diameter, inner_diameter, gap, rotation)

    def to_common_form(self, center_x, center_y, outer_diameter, inner_diameter, gap, rotation):
        # Creates 4 Arc CF units.
        # Note that ARC only works Clockwise.

        # Offset of the arc using
        yoff = gap / 2
        xoff = gap / 2
        arc_center_offset = sqrt((yoff ^ 2) + (xoff ^ 2))
        arc_outer_radius = (outer_diameter / 2) - arc_center_offset
        arc_inner_radius = (inner_diameter / 2) - arc_center_offset

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
            inner_x, inner_y = (arc_center_x - inner_radius, arc_center_y) if "left" in position else (
                arc_center_x, arc_center_y + inner_radius)
        else:
            outer_x, outer_y = (arc_center_x + outer_radius, arc_center_y) if "right" in position else (
                arc_center_x, arc_center_y - outer_radius)
            inner_x, inner_y = (arc_center_x + inner_radius, arc_center_y) if "right" in position else (
                arc_center_x, arc_center_y - inner_radius)

        # Create arc
        self.handle_rotation_and_create_cf_arc(arc_center_x, arc_center_y, outer_x, outer_y, 90, inner_x, inner_y,
                                               rotation)

    def handle_rotation_and_create_cf_arc(self, arc_center_x, arc_center_y, outer_x, outer_y, degree_cw, inner_x,
                                          inner_y, rotation):
        if rotation is not 0:
            arc_center_x, arc_center_y = self.rotate_point_around_origin_cc(arc_center_x, arc_center_y, rotation)
            outer_x, outer_y = self.rotate_point_around_origin_cc(outer_x, outer_y, rotation)
            inner_x, inner_y = self.rotate_point_around_origin_cc(inner_x, inner_y, rotation)

        new_cf_instruction = CFArcTrace(arc_center_x, arc_center_y, outer_x, outer_y, degree_cw, inner_x, inner_y)
        self.common_form.append(new_cf_instruction)
