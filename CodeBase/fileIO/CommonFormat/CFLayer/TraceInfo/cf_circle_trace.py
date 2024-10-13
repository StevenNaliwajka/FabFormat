from CodeBase.fileIO.CommonFormat.CFLayer.TraceInfo.cf_complex_parent import CFComplexParent


class CFCircleTrace(CFComplexParent):
    def __init__(self, radius, size, center_x_y, hole_diameter=0):
        super().__init__()
        self.type = "c"
        self.radius = radius
        self.size = size
        self.center = center_x_y
        self.hole_diameter = hole_diameter
