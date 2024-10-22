from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_trace_parent import CFTraceParent


class CFComplexParent(CFTraceParent):
    def __init__(self):
        super().__init__()
        # Complex shapes, Polygons, Circles.

        # Infil determines if insides are filled. # 0:No infill(DEFAULT), 1: Fill w/ Material
        self.infill = 0

