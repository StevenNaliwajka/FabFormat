from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_complex_parent import CFComplexParent


class CFCircleTrace(CFComplexParent):
    def __init__(self, size_of_line, radius, center_x_y, infill=0, omitted_hole=None):
        super().__init__()
        self.type = "c"
        self.size_of_line = size_of_line
        self.radius = radius
        self.point_list.append(center_x_y)
        self.omitted_hole = omitted_hole
        self.infill = infill  # 0:No infill, 1: Fill w/ Material
