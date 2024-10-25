from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_complex_parent import CFComplexParent
from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_trace_parent import CFTraceParent


class CFArcTrace(CFComplexParent):
    def __init__(self, size_of_line, start_x, start_y, end_x, end_y, center_x, center_y, radius):
        super().__init__()
        self.type = "a"
        self.size_of_line = size_of_line
        self.point_list.append(start_x_y)
        self.point_list.append(end_x_y)
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
