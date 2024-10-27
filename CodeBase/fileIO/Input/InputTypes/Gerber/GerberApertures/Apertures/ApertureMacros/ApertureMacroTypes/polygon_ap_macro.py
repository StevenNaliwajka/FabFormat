from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon import CFPolygonTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class PolygonAPMacro(APMacroParent):
    def __init__(self, exposure, num_vertices, center_x, center_y, diameter, rotation=0):
        # See Page 66:
        # https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf

        # For Reference on Gerber to Common Form Conversion see picture here:
        # XXX No photo ref, Lazy

        super().__init__()
        self.code = 5
        self.exposure = exposure
        # Rotation in DEG CC
        self.to_common_form(num_vertices, center_x, center_y, diameter, rotation)

    def to_common_form(self, num_vertices, center_x, center_y, diameter, rotation):
        # In this form it's easier to handle the shape definition then handle rotation.
        coordinate_list = []

        # First Point
        new_x = center_x + (diameter/2)
        new_y = center_y
        coordinate_list.append(new_x)
        coordinate_list.append(new_y)

        vertices_degree = 360/num_vertices

        for _ in num_vertices:
            new_x, new_y = self.rotate_point_around_origin_cc(new_x, new_y, vertices_degree)
            coordinate_list.append(new_x)
            coordinate_list.append(new_y)

        if rotation is not 0:
            # Handle Rotation.
            for point in num_vertices:
                # Iterates through each point pair and rotates each.
                current_x = coordinate_list[(point - 1) * 2]
                current_y = coordinate_list[((point - 1) * 2) + 1]
                new_x, new_y = self.rotate_point_around_origin_cc(current_x, current_y, rotation)
                # Set new point
                coordinate_list[(point - 1) * 2] = new_x
                coordinate_list[((point - 1) * 2) + 1] = new_y

        new_common_form = CFPolygonTrace(coordinate_list)
        self.common_form.append(new_common_form)