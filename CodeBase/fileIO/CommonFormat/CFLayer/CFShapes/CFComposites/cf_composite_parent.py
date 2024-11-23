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

