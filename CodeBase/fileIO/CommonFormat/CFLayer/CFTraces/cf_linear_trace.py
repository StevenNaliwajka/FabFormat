from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.cf_trace_parent import CFTraceParent


class CFLinearTrace(CFTraceParent):
    def __init__(self, start_x, start_y, end_x, end_y, size_of_line):
        # SEE CurrentCFCheatSheat.PNG in
        # ...CFLayer/Additive/AdditiveTrace/Trace/CurrentCFCheatSheat.png

        super().__init__()
        self.type = "l"
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.size_of_line = size_of_line
