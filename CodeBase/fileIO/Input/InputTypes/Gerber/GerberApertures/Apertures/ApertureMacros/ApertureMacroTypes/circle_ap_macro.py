from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_circle import CFCircle
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class CircleAPMacro(APMacroParent):
    def __init__(self, exposure, diameter, center_x, center_y, unit, rotation=0):
        # See Page 61:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy
        super().__init__(unit)
        self.code = 1
        self.exposure = exposure
        # Rotation in DEG CC
        self.to_common_form(diameter, (center_x, center_y), rotation)

    def to_common_form(self, diameter, center_pt, rotation):
        if rotation is not 0:
            # Handle Rotation.
            new_pt = self.rotate_point_around_origin_cc(center_pt, rotation)
            center_pt = new_pt

        radius = diameter / 2
        new_cf_object = CFCircle(self.unit, center_pt, radius)
        self.common_form.append(new_cf_object)
