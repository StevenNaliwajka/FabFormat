from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.cf_composite_parent import CFCompositeParent


class CFPolygon(CFCompositeParent):
    def __init__(self, unit, primitive_list):
        # SEE CurrentCFCheatSheat.PNG in
        # XXX has to be remade

        # 100% infil

        self.verify_no_curves_in_primitives(primitive_list)

        super().__init__(unit, primitive_list)
        self.type = "pol"

    def verify_no_curves_in_primitives(self, primitive_list):
        for primitive in primitive_list:
            if primitive.type in {"pcs", "sap"}:
                raise TypeError(f"Not allowed to add CF curves to a CF polygon, {primitive.type}: registers as a curve.")

    def _calculate_extreme_points(self):
        for primitive in self.primitive_list:
            self.extreme_points = primitive.get_extreme_points()

    def change_unit(self, new_unit):
        for primitive in self.primitive_list:
            primitive.change_unit()
        self.unit = new_unit