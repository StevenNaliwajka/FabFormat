from CodeBase.fileIO.CommonFormat.CFLayer.TraceInfo.cf_complex_parent import CFComplexParent


class CFPolygonTrace(CFComplexParent):
    def __init__(self, size_of_line, point_list, hole_diameter=0):
        super().__init__()
        self.type = "p"
        self.radius = radius
        self.size = size_of_line
        self.center = center_x_y
        self.hole_diameter = hole_diameter
