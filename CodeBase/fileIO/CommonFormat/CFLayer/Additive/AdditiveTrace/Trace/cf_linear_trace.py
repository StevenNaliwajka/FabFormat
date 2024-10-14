from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_trace_parent import CFTraceParent


class CFLinearTrace(CFTraceParent):
    def __init__(self, size_of_line, start_x_y, end_x_y):
        super().__init__()
        self.type = "l"
        self.size_of_line = size_of_line
        self.point_list.append(start_x_y)
        self.point_list.append(end_x_y)
