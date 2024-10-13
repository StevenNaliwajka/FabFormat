from CodeBase.fileIO.CommonFormat.CFLayer.TraceInfo.cf_trace_parent import CFTraceParent


class CFArcTrace(CFTraceParent):
    def __init__(self, start_x_y, end_x_y, radius):
        super().__init__()
        self.type = "a"
        #TBD
        self.point_list.append(start_x_y)
        self.point_list.append(end_x_y)
        self.radius = radius
