from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class OutlineAPMacro(APMacroParent):
    def __init__(self, exposure, num_vertices, point_list, rotation=0):
        super().__init__()
        self.code = 4
        self.exposure = exposure
        # Rotation in DEG CC
        self.to_common_form(num_vertices, point_list, rotation)

    def to_common_form(self, num_vertices, point_list, rotation):
        if rotation is not 0:
            # Handle Rotation.
            # Num Vertices + 1 Because Start point is not included in count.
            for point in (num_vertices+1):
                # Itterates through each point pair and rotates each.
                current_x = point_list[(point - 1) * 2]
                current_y = point_list[((point - 1) * 2) + 1]
                new_x, new_y = self.rotate_point_around_origin_cc(current_x, current_y, rotation)
                # Set new point
                point_list[(point - 1) * 2] = new_x
                point_list[((point - 1) * 2) + 1] = new_y

        # Create Polygon OBJ
        new_common_form = CFPolygonTrace(point_list)
        self.common_form.append(new_common_form)
