from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_curve_parent import CFCurveParent
from CodeBase.fileIO.CommonFormat.CFOperations.GeneralMath.calculate_distance_p2p import calculate_distance_p2p
from CodeBase.fileIO.CommonFormat.CFOperations.cf_sym_arc_calculations import calculate_sym_arc_degree, \
    get_cf_symmetrical_arc_radius_point, find_sym_arc_radius, generate_points_on_sym_arc_complex


class CFFilledSymmetricalArc(CFCurveParent):
    def __init__(self, unit, center_pt, start_pt, end_pt, arc_radius, inner_off=None):
        # SEE CurrentCFCheatSheat.PNG in
        # ...CFLayer/Additive/AdditiveTrace/Trace/CurrentCFCheatSheat.png

        # NOTES:
        # Inner off always positive. and is a 100% true circular radius so radius is constant
        # Outer Radius is not always true circular but at the middle degree between start/end

        # Always represented as Clockwise.
        qty_points_on_curve = 20
        super().__init__(unit, qty_points_on_curve)
        self.type = "fsa"
        self.center_pt = center_pt
        self.start_pt = start_pt
        self.end_pt = end_pt

        self.edge_radius = calculate_distance_p2p(self.center_pt, self.start_pt)
        self.arc_radius = arc_radius
        # radius can be considered as the radius from the curve to center at the middle degreee between start and end.

        # Inner off always positive. and is a 100% true circular radius so radius is constant
        self.inner_off = inner_off
        # Determines the inner start point
        self.inner_start_pt = find_sym_arc_radius(self.center_pt, self.start_pt, inner_off)
        # Determines the inner end point
        self.inner_end_pt = find_sym_arc_radius(self.center_pt, self.end_pt, inner_off)

        # Determine the degree of the arc
        self.degree = calculate_sym_arc_degree(self.start_pt, self.end_pt, self.center_pt)
        # Determine the radius of the outer arc
        self.radius_pt = get_cf_symmetrical_arc_radius_point(self.degree, self.start_pt, self.center_pt,
                                                             self.arc_radius)
        self.list_of_inner_pts = []

    def _calculate_extreme_points(self):
        # the important numbers are the start of curve, end of curve and the max radius point

        # this is only true if the arc radius is shorter or longer than the start+end radius
        if self.arc_radius != self.edge_radius:
            self.extreme_points.append(self.start_pt)
            self.extreme_points.append(self.radius_pt)
            self.extreme_points.append(self.end_pt)

        # if the arc radius is the same as start+end radius then
        else:
            if self.extreme_points is None:
                self._calculate_points_on_curve()
            self.extreme_points.append(self.list_of_outer_pts)
            self.extreme_points.append(self.list_of_inner_pts)

    def _calculate_points_on_curve(self):
        if self.arc_radius == self.edge_radius:
            self.list_of_outer_pts = self._generate_circular_points(self.center_pt, self.radius_pt, self.start_pt, self.end_pt)
        else:
            generate_points_on_sym_arc_complex(self)
        if self.inner_off is not None:
            self.list_of_inner_pts = self._generate_circular_points(self.center_pt, self.radius_pt, self.start_pt,
                                                                    self.end_pt)

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
        self.list_of_inner_pts = tuple(element * conversion_factor for element in self.list_of_inner_pts)
        self.unit = new_unit

    def shift_cf(self, shift_x, shift_y):
        self.center_pt = (self.center_pt[0] + shift_x, self.center_pt[1] + shift_y)
        self.start_pt = (self.start_pt[0] + shift_x, self.start_pt[1] + shift_y)
        self.end_pt = (self.end_pt[0] + shift_x, self.end_pt[1] + shift_y)
        self.radius_pt = (self.radius_pt[0] + shift_x, self.radius_pt[1] + shift_y)
        for index, pt in enumerate(self.list_of_outer_pts):
             self.list_of_outer_pts[index] = (pt[0]+shift_x, pt[1]+shift_y)
        for index, pt in enumerate(self.list_of_inner_pts):
             self.list_of_inner_pts[index] = (pt[0]+shift_x, pt[1]+shift_y)