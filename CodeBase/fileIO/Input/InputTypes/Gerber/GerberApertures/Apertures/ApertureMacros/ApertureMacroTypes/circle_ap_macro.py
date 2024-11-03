from CodeBase.fileIO.CommonFormat.CFTraces.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class CircleAPMacro(APMacroParent):
    def __init__(self, exposure, diameter, center_x, center_y, rotation=0):
        # See Page 61:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy
        super().__init__()
        self.code = 1
        self.exposure = exposure
        # Rotation in DEG CC
        self.to_common_form(diameter, center_x, center_y, rotation)

    def to_common_form(self, diameter, center_x, center_y, rotation):
        if rotation is not 0:
            # Handle Rotation.
            new_x, new_y = self.rotate_point_around_origin_cc(center_x, center_y, rotation)

            center_x = new_x
            center_y = new_y

        radius = diameter / 2
        new_cf_object = CFCircleTrace(center_x, center_y, radius)
        self.common_form.append(new_cf_object)
