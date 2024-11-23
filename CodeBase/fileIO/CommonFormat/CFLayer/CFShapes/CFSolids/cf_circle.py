from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_shape_parent import CFShapeParent


class CFCircle(CFShapeParent):
    def __init__(self, unit, center_x, center_y, radius, inner_radius=None):
        # SEE CurrentCFCheatSheat.PNG in
        # ...CFLayer/Additive/AdditiveTrace/Trace/CurrentCFCheatSheat.png

        super().__init__(unit)
        self.type = "cir"
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        # If = 0, entire circle is filled. If else, there is a hole in the middle of circle
        if inner_radius > radius:
            raise ValueError(f"CFCircle: Inner Radius of {inner_radius} is larger than the outer radius of {radius}.")
        self.inner_radius = inner_radius
