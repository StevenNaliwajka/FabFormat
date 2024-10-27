import re

from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.ApertureMacros.aperture_macro import \
    ApertureMacro
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.circle_aperture import CircleAperture
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.obround_aperture import ObroundAperture
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.polygon_aperture import PolygonAperture
from CodeBase.fileIO.Input.InputTypes.Gerber.GerberApertures.Apertures.rectangle_aperture import RectangleAperture
from CodeBase.fileIO.Input.InputTypes.input_parent import InputParent
from CodeBase.config.config import Config


# GERBER PARSER TO ALIGN WITH THE UFF (UNIVERSAL FORMAT)
# USING https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf
# AS A BIBLE. PG 19 is table of contents, pg 78 for arcs

class ReadGerber(InputParent):
    def __init__(self, filepath, common_form):
        super().__init__()
        self.filepath = filepath
        self.readfile(filepath)
        self.common_form = common_form

        # Stores apertures. Ordered
        # EX: Aperture #11 is in index 10.
        self.aperture_list = []

        # Stores custom apertures. Holds them until assigned a D code and placed in aperture_list.
        self.aperture_macro_list = []

        # FLAGS
        self._arc_quad_mode = 0  # FLAG. Can be 0 (0-90°), or 1 (0-360°), Specifies how far an arc can turn.
        self._conv_from_polar = 0  # FLAG. set 1 if LP command, must convert cordinates to cartesian(linear) from polar.
        ## ^ WILL BE A FLAG INSIDE OF THE "%FS" Method..... NOT GLOBAL. SET EACH TIME.
        self._current_infill = 0  # FLAG. set 1 if infil of polygon/circle. 0 if empty.
        self._current_tool = None  # "D10" and higher. Used when loading lines into CF. Updated by "D#" Command.
        self._current_line_type = 1  # 1 = "G01":LINEAR, 2 = "G02":Clockwise, 3 = "G03":CounterClockwise.

    def parse_into_cf(self, CONFIG: Config):
        # NEW GERBER PARSER. INPUTS TRACES BY LINE INTO common_form object

        gerber_switcher = {
            ## ORGANIZE  BASED ON WHAT HAPPENS MOST OFTEN... PREVENT IT FROM ITTERATING 10X EVERY TIME.
            "g04": self.do_nothing(),  # COMMENT
            "g74": lambda: setattr(self, 'arc_quad_mode', 0),  # SINGLE QUAD MODE. ARCS 0-90
            "g75": lambda: setattr(self, 'arc_quad_mode', 1),  # MULTI QUAD MODE ARCS 0-360
            "%momm*%": lambda: setattr(self, 'unit', 0),  # METRIC
            "%moin*%": lambda: setattr(self, 'unit', 1),  # INCH
            "%fs": self.format_string(),  # SPECIFIES (LA/LP/IN) AND XY INT:DECIMAL PRECISION **REQ TO CONV TO LA
            "%lpd%": lambda: setattr(self, 'current_infill', 1),  # POLYGONS/CIRCLES FILL INSIDE
            "%lpc%": lambda: setattr(self, 'current_infill', 0),  # POLYGONS/CIRCLES DONT FILL INSIDE
            "%in": self.do_nothing(),  # SETS FILE NAME, CONSIDERED A COMMENT
            "%ippos*%": lambda: setattr(self, 'current_infill', 1),  # DEPRECATED BUT APPEARS THE SAME TO %LPD%
            "%ipneg*%": lambda: setattr(self, 'current_infill', 0),  # DEPRECATED BUT APPEARS THE SAME TO %LPC%
            "%ad": self.create_aperture(),  # Creates an aperture, assigns D code to it.
            "%am": self.create_aperture_macro(),  # BEGINS CREATION OF AN APERTURE MACRO.
            "g36*": xxx,  # BEGINS POLYGON, reads lines till "g37*"
            "x": xxx,  # D01(DRAWS LINE), D02(PEN UP), D03(SINGLE DOT)
            "m02": self.do_nothing(),  # IGNORED. RUNS OFF OF LINES.
            "d": xxx,  # Aperture selection codes, Used to select prior defined apertures. D10 and higher.
            # "g75": self.do_nothing(), # Issued before first circlular plot.
            "g01": lambda: setattr(self, 'current_line_type', 1),  # Swaps to linear plot
            "g02": lambda: setattr(self, 'current_line_type', 2),  # Swaps to clockwise plot
            "g03": lambda: setattr(self, 'current_line_type', 3),  # Swaps to counter-clockwise plot
            # LM
            # LR
            # LS
            # SR
        }

    def create_aperture_macro(self):
        # Creates a Custom Aperture + Populates

        # gets aperture type
        line_data = self.file_by_line_list[self.line]
        match = re.search(r'%am(.*?)\*', line_data)
        aperture_macro_name = match.group(1)

        # Creates new aperture macro
        new_aperture_macro = ApertureMacro(aperture_macro_name)
        # Adds aperture macro to the aperture macro list.
        self.aperture_macro_list.append(new_aperture_macro)
        self.line += 1
        # Iterates through lines till % is reached. Populates the created Aperture
        self.populate_latest_aperture_macro()

        # Must rationalize aperture macro to represent it in a form that General form can understand.
        self.rationalize_latest_aperture_macro()

    def rationalize_latest_aperture_macro(self):
        # Required to represent in a form that General Form can understand.
        current_aperture = self.aperture_macro_list[-1]
        current_aperture.rationalize_aperture_macro()

    def populate_latest_aperture_macro(self):
        # Iterates through the txt file and populated the most recent aperture macro created
        current_aperture = self.aperture_macro_list[-1]
        line_data = self.file_by_line_list[self.line]

        # Define the instruction mapping based on primitive_code
        instruction_map = {
            1: current_aperture.add_circle_instruction,
            20: current_aperture.add_vector_instruction,
            21: current_aperture.add_center_instruction,
            4: current_aperture.add_outline_instruction,
            5: current_aperture.add_polygon_instruction,
            7: current_aperture.add_thermal_instruction
        }

        while "%" not in line_data:
            self.add_primitive_to_aperture_macro(instruction_map, line_data)
            self.line += 1
            line_data = self.file_by_line_list[self.line]
        # Remove the % from the line
        stripped_line_data = line_data[:-1]
        # If its not empty run again
        if stripped_line_data:
            self.add_primitive_to_aperture_macro(instruction_map, line_data)
        # DO NOT append line +=1 again due to the fact that the OG switcher iterates by one upon finishing of method.

    def add_primitive_to_aperture_macro(self, instruction_map, line_data):
        ## POSSIBLY AN ISSUE IN THE FUTURE OF INDENTS BEING WEIRD. I MATCHED ONE USE CASE
        ## NOT PERFECT. IF FILE DOES NOT INDENT AFTER EVERY * THIS WILL NOT WORK....
        ## NOT MY PROBLEM RN... LOL

        stripped_line_data = line_data.rstrip('*')
        numbers = [int(num.strip()) for num in stripped_line_data.split(',')]
        primitive_code = numbers[0]

        if primitive_code in instruction_map:
            # Prepare arguments based on whether rotation is present
            args_without_rotation = numbers[1:-1] if len(numbers) - 1 == len(
                instruction_map[primitive_code].__code__.co_varnames) else numbers[1:]
            rotation = numbers[-1] if len(numbers) - 1 != len(
                instruction_map[primitive_code].__code__.co_varnames) else 0
            instruction_map[primitive_code](*args_without_rotation, rotation)
        elif primitive_code == 0:
            pass  # Comment code; no action required
        else:
            raise ValueError(
                f"READ_GERBER: Line: {self.line}, The inputs for primitive code #{primitive_code} are not valid.")

    def create_aperture(self):
        line_data = self.file_by_line_list[self.line]
        aperture_number, aperture_type = self.extract_aperture_info(line_data)

        if aperture_type == "c":
            new_aperture = self.create_circle_aperture(aperture_number, line_data)
        elif aperture_type == "r":
            new_aperture = self.create_rectangle_aperture(aperture_number, line_data)
        elif aperture_type == "o":
            new_aperture = self.create_obround_aperture(aperture_number, line_data)
        elif aperture_type == "p":
            new_aperture = self.create_polygon_aperture(aperture_number, line_data)
        else:
            new_aperture = self.create_macro_aperture(aperture_number, aperture_type)

        if new_aperture:
            self.add_to_aperture_list(new_aperture)
        else:
            raise ValueError(f"READ_GERBER: Line: {self.line}, Aperture type \"{aperture_type}\" is not valid.")

    def extract_aperture_info(self, line_data):
        match = re.search(r'\d+([a-zA-Z]+)[*,]', line_data)
        num_match = re.search(r'\d+', line_data)

        if match and num_match:
            aperture_number = num_match.group()
            aperture_type = match.group(1)
            return aperture_number, aperture_type
        else:
            raise ValueError(f"No valid number or aperture type found in line #{self.line}: \"{line_data}\"")

    def create_circle_aperture(self, aperture_number, line_data):
        pattern = r",([0-9]*\.?[0-9]+)(x([0-9]*\.?[0-9]+))?"
        match = re.search(pattern, line_data)
        if match:
            diameter = float(match.group(1))
            inside_hole_diameter = float(match.group(3)) if match.group(3) else None
            return CircleAperture(aperture_number, diameter, inside_hole_diameter)
        else:
            raise ValueError("Circle aperture string format error.")

    def create_rectangle_aperture(self, aperture_number, line_data):
        pattern = r",([0-9]*\.?[0-9]+)x([0-9]*\.?[0-9]+)(x([0-9]*\.?[0-9]+))?"
        match = re.search(pattern, line_data)
        if match:
            x_size = float(match.group(1))
            y_size = float(match.group(2))
            inside_hole_diameter = float(match.group(4)) if match.group(4) else None
            return RectangleAperture(aperture_number, x_size, y_size, inside_hole_diameter)
        else:
            raise ValueError("Rectangle aperture string format error.")

    def create_obround_aperture(self, aperture_number, line_data):
        pattern = r",([0-9]*\.?[0-9]+)x([0-9]*\.?[0-9]+)(x([0-9]*\.?[0-9]+))?"
        match = re.search(pattern, line_data)
        if match:
            x_size = float(match.group(1))
            y_size = float(match.group(2))
            inside_hole_diameter = float(match.group(4)) if match.group(4) else None
            return ObroundAperture(aperture_number, x_size, y_size, inside_hole_diameter)
        else:
            raise ValueError("Obround aperture string format error.")

    def create_polygon_aperture(self, aperture_number, line_data):
        pattern = r",([0-9]*\.?[0-9]+)X([0-9]*\.?[0-9]+)(X([0-9]*\.?[0-9]+))?(X([0-9]*\.?[0-9]+))?"
        match = re.search(pattern, line_data)
        if match:
            outer_diameter = float(match.group(1))
            num_vertices = float(match.group(2))
            rotation = float(match.group(4)) if match.group(4) else None
            inside_hole_diameter = float(match.group(6)) if match.group(6) else None
            return PolygonAperture(aperture_number, outer_diameter, num_vertices, rotation, inside_hole_diameter)
        else:
            raise ValueError("Polygon aperture string format error.")

    def create_macro_aperture(self, aperture_number, aperture_type):
        for aperture_macro in self.aperture_macro_list:
            if aperture_type == aperture_macro.name:
                return aperture_macro(aperture_number)
        return None

    def add_to_aperture_list(self, new_aperture):
        index = new_aperture.aperture_number
        # APERTURE LIST IS ORDERED, Adds Aperture based on the number
        # EX: Aperture #10 is in index 9.
        if len(self.aperture_list) <= index:
            self.aperture_list.extend([None] * (index + 1 - len(self.aperture_list)))
        self.aperture_list[index - 1] = new_aperture

    def format_string(self):
        match = re.search(r'x(\d)(\d)y(\d)(\d)', self.file_by_line_list[self.line])
        ## LA/LP/IN NOT IMPLEMENTED
        if match:
            x1, x2, y1, y2 = match.groups()
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)

            self.x_number_format = f"{x1}:{x2}"
            self.y_number_format = f"{y1}:{y2}"
        else:
            raise ValueError("String does not match the expected format")

    @property
    def conv_from_polar(self):
        return self._conv_from_polar

    @property
    def arc_quad_mode(self):
        return self._arc_quad_mode

    @property
    def current_infill(self):
        return self._current_infill

    @property
    def current_tool(self):
        return self._current_tool

    @property
    def current_line_type(self):
        return self.current_line_type

    @conv_from_polar.setter
    def conv_from_polar(self, new_value):
        if new_value in (0, 1):
            self._conv_from_polar = new_value

    @arc_quad_mode.setter
    def arc_quad_mode(self, new_value):
        if new_value in (0, 1):
            self._arc_quad_mode = new_value

    @current_infill.setter
    def current_infill(self, new_value):
        if new_value in (0, 1):
            self._current_infill = new_value

    @current_tool.setter
    def current_tool(self, new_value):
        in_number_part = new_value[1:]
        # ALSO CHECK FOR BOARD EXISTING ************
        if in_number_part >= 10:
            self._current_tool = new_value

    @current_line_type.setter
    def current_line_type(self, new_value):
        if new_value in (1, 2, 3):
            self._current_line_type = new_value