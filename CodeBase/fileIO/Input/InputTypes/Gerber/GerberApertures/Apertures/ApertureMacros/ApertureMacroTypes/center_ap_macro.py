from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class CenterAPMacro(APMacroParent):
    def __init__(self, exposure, width, height, center_x, center_y, unit, rotation=0):
        # See Page 63:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy

        super().__init__(unit)
        self.code = 21
        self.exposure = exposure
        # Rotation in DEG CC
        self.to_common_form(width, height, (center_x, center_y), rotation)

    def to_common_form(self, width, height, center_pt, rotation):
        self.am_create_rectangle_cf(width, height, center_pt, rotation)
