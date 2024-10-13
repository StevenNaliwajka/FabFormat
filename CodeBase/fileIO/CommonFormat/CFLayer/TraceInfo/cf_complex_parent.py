from CodeBase.fileIO.CommonFormat.CFLayer.TraceInfo.cf_trace_parent import CFTraceParent


class CFComplexParent(CFTraceParent):
    def __init__(self):
        super().__init__()
        # ALLOWS FOR SPECIFYING OF omitted trace type. If Infil is true.
        # Another smaller circle/polygon can be added here.
        # Allows for future scalability. Gerber only supports circle insides, other shapes too
        self.omittedhole = None
        # Infil determines if insides are filled. 1 = T, 0 = F (DEFAULT)
        self.infill = 0

