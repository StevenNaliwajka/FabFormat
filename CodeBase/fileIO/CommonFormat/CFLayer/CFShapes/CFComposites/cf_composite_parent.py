from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_shape_parent import CFShapeParent


class CFCompositeParent(CFShapeParent):
    def __init__(self, unit, primitive_list):
        # Composite Shapes made up of primitives shapes.
        super().__init__(unit)

        # Verifies continuity and no intersections.
        self.verify_composite_continuity(primitive_list)
        self.verify_composite_intersections(primitive_list)

        self.primitive_list = primitive_list

    def verify_composite_continuity(self, primitive_list):
        # verifies that composite methods are continuous
        pass

    def verify_composite_intersections(self, primitive_list):
        # verifies composites dont intersect.
        pass

    def shift_cf(self, shift_x, shift_y):
        for primitive in self.primitive_list:
            primitive.shift_cf(shift_x, shift_y)

    def get_bounding_box(self):
        bounding_box_list = []
        for cf in self.primitive_list:
            bounding_box_list.append(cf.get_bounding_box())
        return bounding_box_list

    def change_unit(self, new_unit):
        for primitive in self.primitive_list:
            primitive.change_unit()
        self.unit = new_unit

    def _calculate_extreme_points(self):
        for primitive in self.primitive_list:
            self.extreme_points = primitive.get_extreme_points()