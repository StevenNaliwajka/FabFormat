from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.ap_macro_parent import \
    APMacroParent


class CenterAPMacro(APMacroParent):
    def __init__(self, exposure, width, height, center_x, center_y, rotation=0):
        super().__init__()
        self.code = 21
        self.exposure = exposure
        self.width = width
        self.height = height
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation  # IN DEGREES CC
        self.common_form = []

        self.to_common_form()

    def to_common_form(self):
        if self.rotation is not 0:
            # Handle Rotation.
            new_x, new_y = self.rotate_point_around_origin_cc(self.center_x, self.center_y, self.rotation)

            self.center_x = new_x
            self.center_y = new_y
            self.rotation = 0

        coordinate_list = []
        ## VERIFY THIS MAY BE WRONG
        # Convert to polygon. Solve for vertices.
        # Bottom left
        new_x_cordinate = self.center_x - (self.width / 2)
        new_y_cordinate = self.center_y - (self.height / 2)
        coordinate_list.append(new_x_cordinate)
        coordinate_list.append(new_y_cordinate)
        # Top left
        new_y_cordinate = new_y_cordinate + self.height
        coordinate_list.append(new_x_cordinate)
        coordinate_list.append(new_y_cordinate)
        # Top right
        new_x_cordinate = new_x_cordinate + self.height
        coordinate_list.append(new_x_cordinate)
        coordinate_list.append(new_y_cordinate)
        # Bottom Right
        new_y_cordinate = new_y_cordinate - self.height
        coordinate_list.append(new_x_cordinate)
        coordinate_list.append(new_y_cordinate)

        # Create Polygon OBJ
        self.common_form = CFPolygonTrace(coordinate_list)
