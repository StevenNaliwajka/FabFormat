from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.cf_trace_parent import CFTraceParent


class CFComplexParent(CFTraceParent):
    def __init__(self, unit):
        super().__init__(unit)
        # Complex shapes, Polygons, Circles.

        # Infil determines if insides are filled. # 0:No infill(DEFAULT), 1: Fill w/ Material
        self.infill = 0

