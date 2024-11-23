from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_shape_parent import CFShapeParent


class CFLinearPrim(CFShapeParent):
    def __init__(self, unit, start_x, start_y, end_x, end_y):
        # SEE CurrentCFCheatSheat.PNG in
        # CHANGED. ONLY STORED AS A Line WITH ZERO SIZE. USED FOR BOUNDING WITH POLYGONS.

        super().__init__(unit)
        self.type = "lin"
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
