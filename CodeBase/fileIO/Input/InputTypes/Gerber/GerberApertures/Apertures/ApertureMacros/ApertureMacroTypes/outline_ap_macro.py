from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class OutlineAPMacro(APMacroParent):
    def __init__(self, exposure, num_vertices, point_list, rotation=0):
        super().__init__()
        self.code = 4
        self.exposure = exposure
        # Num Vertices + 1 Because Start point is not included in count.
        self.num_vertices = num_vertices + 1
        self.point_list = point_list
        self.rotation = rotation  # IN DEGREES CC
        self.common_form = []

        self.to_common_form()

    def to_common_form(self):
        if self.rotation is not 0:
            # Handle Rotation.
            for point in self.num_vertices:
                # Itterates through each point pair and rotates each.
                current_x = self.point_list[(point - 1) * 2]
                current_y = self.point_list[((point - 1) * 2) + 1]
                new_x, new_y = self.rotate_point_around_origin_cc(current_x, current_y, self.rotation)
                # Set new point
                self.point_list[(point - 1) * 2] = new_x
                self.point_list[((point - 1) * 2) + 1] = new_y
            self.rotation = 0

        # Create Polygon OBJ
        self.common_form = CFPolygonTrace(self.point_list)
