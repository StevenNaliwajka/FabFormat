from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_curve_parent import CFCurveParent
from CodeBase.fileIO.CommonFormat.CFOperations.GeneralMath.calculate_distance_p2p import calculate_distance
from CodeBase.fileIO.CommonFormat.CFOperations.cf_sym_arc_calculations import calculate_sym_arc_degree, \
    get_cf_symmetrical_arc_radius_point


class CFSymmetricalArcPrim(CFCurveParent):
    def __init__(self, unit, center_pt, start_pt, end_pt, arc_radius):
        # Re-learning Trig for figuring out the best way to store arc data has been fun. See reference picture for my
        # take on it. There are probably better/more concise ways to store arc data. Let me know if any math person
        # knows a better solution.

        # segment of a circle

        # ALWAYS CLOCKWISE
        # SEE CurrentCFCheatSheat.PNG in
        # ...CFLayer/Additive/AdditiveTrace/Trace/CurrentCFCheatSheat.png
        qty_points_on_curve = 20
        super().__init__(unit, qty_points_on_curve)
        self.type = "sap"
        self.center_pt = center_pt
        self.start_pt = start_pt
        self.end_pt = end_pt

        self.edge_radius = calculate_distance(center_pt, start_pt)
        self.arc_radius = arc_radius

        self.degree = calculate_sym_arc_degree(start_pt, end_pt, center_pt)
        self.radius_pt = get_cf_symmetrical_arc_radius_point(self.degree, self.start_pt, self.center_pt,
                                                             self.arc_radius)

    def _calculate_extreme_points(self):
        # the important numbers are the start of curve, end of curve and the max radius point

        # this is only true if the arc radius is shorter or longer than the start+end radius
        if self.arc_radius != self.edge_radius:
            self.extreme_points.append(self.start_pt)
            self.extreme_points.append(self.radius_pt)
            self.extreme_points.append(self.end_pt)

        # if the arc radius is the same as start+end radius then
        else:
            if self.list_of_outer_pts is None:
                self._calculate_points_on_curve()
            self.extreme_points.append(self.list_of_outer_pts)

    def _calculate_points_on_curve(self):
        self.list_of_outer_pts = self._generate_circular_points(self.center_pt, self.radius_pt, self.start_pt, self.end_pt)

    def change_unit(self, new_unit):
        conversion_factor = None
        if new_unit == "mm":
            conversion_factor = 0.0393701
        else:
            conversion_factor: 25.4
        self.center_pt = tuple(element * conversion_factor for element in self.center_pt)
        self.start_pt = tuple(element * conversion_factor for element in self.start_pt)
        self.end_pt = tuple(element * conversion_factor for element in self.end_pt)
        self.arc_radius = self.arc_radius * conversion_factor
        self.edge_radius = self.edge_radius * conversion_factor
        self.radius_pt = tuple(element * conversion_factor for element in self.radius_pt)
        self.list_of_outer_pts = tuple(element * conversion_factor for element in self.list_of_outer_pts)
        self.unit = new_unit

    def shift_cf(self, shift_x, shift_y):
        self.center_pt = (self.center_pt[0] + shift_x, self.center_pt[1] + shift_y)
        self.start_pt = (self.start_pt[0] + shift_x, self.start_pt[1] + shift_y)
        self.end_pt = (self.end_pt[0] + shift_x, self.end_pt[1] + shift_y)
        self.radius_pt = (self.radius_pt[0] + shift_x, self.radius_pt[1] + shift_y)
        for index, pt in enumerate(self.list_of_outer_pts):
             self.list_of_outer_pts[index] = (pt[0]+shift_x, pt[1]+shift_y)
