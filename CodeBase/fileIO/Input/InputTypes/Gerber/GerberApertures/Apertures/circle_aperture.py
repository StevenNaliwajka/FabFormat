from CodeBase.fileIO.CommonFormat.CFTraces.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent


class CircleAperture(ApertureParent):
    def __init__(self, ap_number, diameter, inside_hole_diam):
        # See Page 51:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No Photo Ref. Lazy

        super().__init__()
        self.aperture_type = "c"
        self.aperture_number = ap_number
        self.to_common_form(diameter, inside_hole_diam)

    def to_common_form(self, diameter, inside_hole_diam):
        new_common_form = CFCircleTrace(0, 0, (diameter / 2), inside_hole_diam)
        self.common_form.append(new_common_form)
