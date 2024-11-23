from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_shape_parent import CFShapeParent
from CodeBase.fileIO.CommonFormat.CFOperations.GeneralMath.calculate_distance_p2p import calculate_distance
from CodeBase.fileIO.CommonFormat.CFOperations.cf_sym_arc_calculations import calculate_sym_arc_degree, \
    get_cf_symmetrical_arc_radius_point


class CFSymmetricalArcPrim(CFShapeParent):
    def __init__(self, unit, c_x, c_y, s_x, s_y, e_x, e_y, arc_radius):
        # Re-learning Trig for figuring out the best way to store arc data has been fun. See reference picture for my
        # take on it. There are probably better/more concise ways to store arc data. Let me know if any math person
        # knows a better solution.

        # segment of a circle

        # ALWAYS CLOCKWISE
        # SEE CurrentCFCheatSheat.PNG in
        # ...CFLayer/Additive/AdditiveTrace/Trace/CurrentCFCheatSheat.png

        super().__init__(unit)
        self.type = "sap"
        self.center_x = c_x
        self.center_y = c_y
        self.start_x = s_x
        self.start_y = s_y
        self.end_x = e_x
        self.end_y = e_y
        self.arc_radius = arc_radius

        self.edge_radius = calculate_distance(c_x, c_y, s_x, s_y)
        self.arc_radius = arc_radius

        self.degree = calculate_sym_arc_degree((s_x, s_y), (e_x, e_y), (c_x, c_y))
        self.radius_x, self.radius_y = get_cf_symmetrical_arc_radius_point(self.degree, (s_x, s_y),
                                                                           (c_x, c_y), arc_radius)