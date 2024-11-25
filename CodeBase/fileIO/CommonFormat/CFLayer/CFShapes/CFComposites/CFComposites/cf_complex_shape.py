from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.cf_composite_parent import CFCompositeParent


class CFComplexShape(CFCompositeParent):
    def __init__(self, unit, primitive_list):
        # SEE CurrentCFCheatSheat.PNG in
        # XXX has to be remade

        # 100% infil
        super().__init__(unit, primitive_list)
        self.type = "com"

    def _calculate_extreme_points(self):
        for primitive in self.primitive_list:
            self.extreme_points = primitive.get_extreme_points()

    def change_unit(self, new_unit):
        for primitive in self.primitive_list:
            primitive.change_unit()
        self.unit = new_unit