from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class PolygonAPMacro(APMacroParent):
    def __init__(self, exposure, num_vertices, center_x, center_y, diameter, rotation=0):
        super().__init__()
        self.code = 5
        self.exposure = exposure
        self.num_vertices = num_vertices
        self.center_x = center_x
        self.center_y = center_y
        self.diameter = diameter
        self.rotation = rotation  # IN DEGREES CC
        self.common_form = []

        self.to_common_form()

    def to_common_form(self):
        # In this form it's easier to handle the shape definition then handle rotation.
        coordinate_list = []

        # First Point
        new_x = self.center_x + (self.diameter/2)
        new_y = self.center_y
        coordinate_list.append(new_x)
        coordinate_list.append(new_y)

        vertices_degree = 360/self.num_vertices

        for vertice in self.num_vertices:
            new_x, new_y = self.rotate_point_around_origin_cc(new_x, new_y, vertices_degree)
            coordinate_list.append(new_x)
            coordinate_list.append(new_y)

        if self.rotation is not 0:
            # Handle Rotation.
            for point in self.num_vertices:
                # Iterates through each point pair and rotates each.
                current_x = coordinate_list[(point - 1) * 2]
                current_y = coordinate_list[((point - 1) * 2) + 1]
                new_x, new_y = self.rotate_point_around_origin_cc(current_x, current_y, self.rotation)
                # Set new point
                coordinate_list[(point - 1) * 2] = new_x
                coordinate_list[((point - 1) * 2) + 1] = new_y
            self.rotation = 0

        self.common_form = CFPolygonTrace(coordinate_list)
