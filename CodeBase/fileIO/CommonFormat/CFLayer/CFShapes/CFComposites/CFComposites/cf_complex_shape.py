from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.cf_composite_parent import CFCompositeParent


class CFComplexShape(CFCompositeParent):
    def __init__(self, unit, primitive_list):
        # SEE CurrentCFCheatSheat.PNG in
        # XXX has to be remade

        # 100% infil
        super().__init__(unit, primitive_list)
        self.type = "com"