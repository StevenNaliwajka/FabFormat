from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.cf_complex_parent import CFComplexParent


class CFPolygonTrace(CFComplexParent):
    def __init__(self, unit, point_list):
        # SEE CurrentCFCheatSheat.PNG in
        # ...CFLayer/Additive/AdditiveTrace/Trace/CurrentCFCheatSheat.png

        super().__init__(unit)
        self.type = "p"
        # 100% INFILL. IF YOU NEED A HOLE. SLICE THE SHAPE INTO MULTIPLE PARTS.
        # POINT LIST STARTS AND ENDS AT SAME POINTS.
        # POINT LIST SAVED AS [x1, y1, x2, y2 ...]
        if point_list[0] is not point_list[-1]:
            raise ValueError(f"CFPolygon: Start({point_list[0]}) and end({point_list[-1]}) X cordinates of CF"
                             f" polygon do not match.")
        if point_list[1] is not point_list[-2]:
            raise ValueError(f"CFPolygon: Start({point_list[1]}) and end({point_list[-2]}) Y cordinates of CF"
                             f" polygon do not match.")
        self.point_list = point_list
