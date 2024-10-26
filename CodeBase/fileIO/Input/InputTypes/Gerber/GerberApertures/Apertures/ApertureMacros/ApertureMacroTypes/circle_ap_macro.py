from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class CircleAPMacro(APMacroParent):
    def __init__(self, exposure, diameter, center_x, center_y, rotation=0):
        super().__init__()
        self.code = 1
        self.exposure = exposure
        self.diameter = diameter
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation  # IN DEGREES CC
        self.common_form = []

        self.to_common_form()

    def to_common_form(self):
        if self.rotation is not 0:
            # Handle Rotation.
            new_x, new_y = self.rotate_point_around_origin_cc(self.center_x, self.center_y, self.rotation)

            self.center_x = new_x
            self.center_y = new_y
            self.rotation = 0

        radius = self.diameter/2
        new_cf_object = CFCircleTrace(self.center_x, self.center_y, radius)
        self.common_form = new_cf_object