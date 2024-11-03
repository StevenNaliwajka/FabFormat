from CodeBase.fileIO.CommonFormat.CFTraces.cf_complex_parent import CFComplexParent


class CFSymmetricalArcTrace(CFComplexParent):
    def __init__(self, c_x, c_y, s_x, s_y, e_x, e_y, radius, inner_off=None):
        # Re-learning Trig for figuring out the best way to store arc data has been fun. See reference picture for my
        # take on it. There are probably better/more concise ways to store arc data. Let me know if any math person
        # knows a better solution.

        # ALWAYS CLOCKWISE
        # SEE CurrentCFCheatSheat.PNG in
        # ...CFLayer/Additive/AdditiveTrace/Trace/CurrentCFCheatSheat.png

        super().__init__()
        self.type = "a"
        self.center_x = c_x
        self.center_y = c_y
        self.start_x = s_x
        self.start_y = s_y
        # Degree is always Clockwise. Determines the angle that the radius has.
        self.end_x = e_x
        self.end_y = e_y
        self.radius = radius
        # Inner off always positive.
        self.inner_off = inner_off
