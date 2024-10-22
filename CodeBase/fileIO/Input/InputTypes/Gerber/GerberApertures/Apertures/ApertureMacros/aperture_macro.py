from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.center_ap_macro import \
    CenterAPMacro
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.circle_ap_macro import \
    CircleAPMacro
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.outline_ap_macro import \
    OutlineAPMacro
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.polygon_ap_macro import \
    PolygonAPMacro
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.thermal_ap_macro import \
    ThermalAPMacro
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.ApertureMacroTypes.vector_ap_macro import \
    VectorAPMacro
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.aperture_parent import ApertureParent


class ApertureMacro(ApertureParent):
    def __init__(self, ap_type):
        super().__init__()
        # A custom Aperture Macro, In the same category as the standard circle, obround, polygon
        # and rectangle. The issue is that has multiple types subshapes associated with it. But those types
        # have the option to override each other and or rotate. The fact that they can rotate and dont have infil
        # prevents me from using the existing 4 shapes. gotta make custom ones. :(

        # Aperture type, stored the same as typ. obround, polygon, circle, rectangle
        self.aperture_type = ap_type
        # Meat: All aperture instructions. Should be read left to right due to the fact of overwriting.
        self.aperture_instructions = []
        self.rationalized_instructions = []

    def assign_aperture_number(self, ap_number):
        # when aperture is created, no number
        # when it's done created it then has the option of being assigned a D code.
        self.aperture_number = ap_number

    def rationalize_aperture_macro(self):
        # This thing was a bitch to figure out. Lots of geometry and just sitting starting into the distance.
        # PLAN,
        # 1) CONVERT APERTURE DATA TO FORMULAS.... IN THE OBJECT

        # 2) Check if the formulas intersect using below method.
        # Half Matrix..
        #    1 2 3 4
        #  1 x ? ? ?
        #  2 x x ? ?
        #  3 x x x ?
        #  4 x x x x
        # 1 is converted to common form shapes and placed into rationalized_instructions
        # -If 2 is exposure of 0, remove overlap parts from 1. 1's broken up new pieces get replaced
        # in rationalized_instructions.
        # -else. convert to common form shapes and place into rationalized_instructions
        # rinse and repeat for 3, 4, etc..
        # Circles that are sliced and have chunks removed are converted into Arcs.
        # DONT CARE ABOUT SHAPES OVERLAPING. PERFORMANCE ORIENTED FOR LATER.
        # IF SHAPE OVERLAP DOES NOT MATTER WE DONT WANT TO COMPUTE TILL ABSOLUTELY NECESSARY.
        # EX, .GCODE will need to be parsed to prevent overlap.
        # However, a .png will not matter.
        # This strategy will be used to solve for overlap in common form later. The difference between here
        # and there is that this also converts unique shapes to common form shapes.
        # CF overlap will be a copy of the first part here.

    def add_circle_instruction(self, exposure, diameter, center_x, center_y, rotation):
        new_instruction = CircleAPMacro(exposure, diameter, center_x, center_y, rotation)
        self.aperture_instructions.append(new_instruction)

    def add_vector_instruction(self, exposure, width, start_x, start_y, end_x, end_y, rotation):
        new_instruction = VectorAPMacro(exposure, width, start_x, start_y, end_x, end_y, rotation)
        self.aperture_instructions.append(new_instruction)

    def add_center_instruction(self, exposure, width, height, center_x, center_y, rotation):
        new_instruction = CenterAPMacro(exposure, width, height, center_x, center_y, rotation)
        self.aperture_instructions.append(new_instruction)

    def add_outline_instruction(self, exposure, num_vertices, start_x, start_y, point_list, rotation):
        new_instruction = OutlineAPMacro(exposure, num_vertices, start_x, start_y, point_list, rotation)
        self.aperture_instructions.append(new_instruction)

    def add_polygon_instruction(self, exposure, num_vertices, center_x, center_y, diameter, rotation):
        new_instruction = PolygonAPMacro(exposure, num_vertices, center_x, center_y, diameter, rotation)
        self.aperture_instructions.append(new_instruction)

    def add_thermal_instruction(self, center_x, center_y, outer_diameter, inner_diameter, gap, rotation):
        new_instruction = ThermalAPMacro(center_x, center_y, outer_diameter, inner_diameter, gap, rotation)
        self.aperture_instructions.append(new_instruction)
