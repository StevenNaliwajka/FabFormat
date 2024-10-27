from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent


class CircleAperture(ApertureParent):
    def __init__(self, ap_number, diameter, inside_hole_diam):
        super().__init__()
        self.aperture_type = "c"
        self.aperture_number = ap_number
        self.to_common_form(diameter, inside_hole_diam)

    def to_common_form(self, diameter, inside_hole_diam):
        new_common_form = CFCircleTrace(0, 0, (diameter / 2), inside_hole_diam)
        self.common_form.append(new_common_form)
