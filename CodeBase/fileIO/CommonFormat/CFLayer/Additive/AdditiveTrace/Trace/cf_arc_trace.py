from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_complex_parent import CFComplexParent
from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_trace_parent import CFTraceParent


class CFArcTrace(CFComplexParent):
    def __init__(self, center_x, center_y, outer_start_x, outer_start_y, outer_end_x, outer_end_y, inner_dif):
        super().__init__()
        self.type = "a"
        self.center_x = center_x
        self.center_y = center_y
        self.outer_x = outer_x
        self.outer_y = outer_y
        # Degree is always Clockwise. Determines the angle that the radius has.
        self.degree_cw = degree_cw
        self.inner_x = inner_x
        self.inner_y = inner_y
