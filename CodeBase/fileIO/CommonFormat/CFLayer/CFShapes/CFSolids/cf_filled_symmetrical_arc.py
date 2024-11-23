from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_shape_parent import CFShapeParent
from CodeBase.fileIO.CommonFormat.CFOperations.GeneralMath.calculate_distance_p2p import calculate_distance
from CodeBase.fileIO.CommonFormat.CFOperations.cf_determine_furthest_point import _calculate_distance
from CodeBase.fileIO.CommonFormat.CFOperations.cf_sym_arc_calculations import calculate_sym_arc_degree, \
    get_cf_symmetrical_arc_radius_point


class CFFilledSymmetricalArc(CFShapeParent):
    def __init__(self, unit, c_x, c_y, s_x, s_y, e_x, e_y, arc_radius, inner_off=None):
        # SEE CurrentCFCheatSheat.PNG in
        # ...CFLayer/Additive/AdditiveTrace/Trace/CurrentCFCheatSheat.png

        super().__init__(unit)
        self.type = "fsa"
        self.center_x = c_x
        self.center_y = c_y
        self.start_x = s_x
        self.start_y = s_y
        # Degree is always Clockwise. Determines the angle that the radius has.
        self.end_x = e_x
        self.end_y = e_y

        self.edge_radius = calculate_distance(c_x, c_y, s_x, s_y)
        self.arc_radius = arc_radius
        # radius can be considered as the radius from the curve to center at the middle degreee between start and end.

        # Inner off always positive.
        self.inner_off = inner_off

        self.degree = calculate_sym_arc_degree((s_x, s_y), (e_x, e_y), (c_x, c_y))
        self.radius_x, self.radius_y = get_cf_symmetrical_arc_radius_point(self.degree, (s_x, s_y),
                                                                           (c_x, c_y), arc_radius)
