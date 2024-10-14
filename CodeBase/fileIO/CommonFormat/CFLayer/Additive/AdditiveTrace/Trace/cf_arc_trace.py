from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_trace_parent import CFTraceParent


class CFArcTrace(CFTraceParent):
    def __init__(self, size_of_line, start_x_y, end_x_y, radius):
        super().__init__()
        self.type = "a"
        self.size_of_line = size_of_line
        self.point_list.append(start_x_y)
        self.point_list.append(end_x_y)
        self.radius = radius
