from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.cf_complex_parent import CFComplexParent


class CFPolygonTrace(CFComplexParent):
    def __init__(self, size_of_line, point_list, infill=0, omitted_hole=None):
        super().__init__()
        self.type = "p"
        self.size_of_line = size_of_line
        self.point_list.append(point_list)
        self.omitted_hole = omitted_hole
        self.infill = infill  # 0:No infill, 1: Fill w/ Material
