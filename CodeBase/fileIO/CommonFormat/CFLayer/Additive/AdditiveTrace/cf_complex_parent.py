from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_trace_parent import CFTraceParent


class CFComplexParent(CFTraceParent):
    def __init__(self):
        super().__init__()
        # Complex shapes, Polygons, Circles.

        # ALLOWS FOR SPECIFYING OF omitted trace type.
        # Another smaller circle/polygon can be added as an 'omitted' shape if the infill = 1
        self.omitted_hole = None
        # Infil determines if insides are filled. # 0:No infill(DEFAULT), 1: Fill w/ Material
        self.infill = 0

