from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class VectorAPMacro(APMacroParent):
    def __init__(self, exposure, width, start_x, start_y, end_x, end_y, rotation=0):
        super().__init__()
        self.code = 20
        self.exposure = exposure
        self.width = width
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.rotation = rotation  # IN DEGREES CC
        self.common_form = []

        self.to_common_form()

    def to_common_form(self):
        coordinate_list = []
        # Convert to polygon. Solve for vertices.
        # Bottom left
        new_x_coordinate = self.start_x
        new_y_coordinate = self.start_y - (self.width/2)
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        # Top left
        new_y_coordinate = self.start_y + self.width
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        # Top right
        new_x_coordinate = self.end_y
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        # Bottom Right
        new_y_coordinate = self.start_y - self.width
        coordinate_list.append(new_x_coordinate)
        coordinate_list.append(new_y_coordinate)

        # Create Polygon OBJ
        self.common_form = CFPolygonTrace(coordinate_list)

