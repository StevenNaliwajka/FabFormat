import re

from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.Input.InputTypes.input_parent import InputParent


# REWRITTEN EXCELLON DRILL PARSER.
# GTG.py's version was lackluster and did not support EAGLE's default .XLN drill file.
# Could be me doing stuff wrong. But its better now.
# I re-wrote to be more legible and flexible.

## CORRECT TO USE CF STANDARD CIRCLES....

class ReadExcellonDrill(InputParent):
    def __init__(self, excellon_drill_config, common_form):
        super().__init__(excellon_drill_config.filepath, excellon_drill_config.layer_type, excellon_drill_config.active_layers, common_form)

        self.current_drill = "T1"  # DEFAULT T1

        self.number_format = None

        self.drill_tool_diameter = []

    def parse_into_cf(self):
        # SWITCHER OF EXCELLON HEADER SYNTAX OPTIONS.
        # IF CONFUSED ON VARS. SEE "universal_parent.py"

        # BULK OF THE PARSER IS IN THESE TWO SWITCHERS.
        # THE "BRAIN"... IF THE STRINGS ARE FOUND WHILE GOING LINE BY LINE IN FILE.
        # RUN ASSOCIATED METHOD.
        # https://gist.github.com/katyo/5692b935abc085b1037e USED AS REF TO BACKFILL MY EXISTING FILES.
        # NOT 100%, BARE BONES. CLOSER TO 40% OF AVAILABLE EXCELLON FUNCTIONALITY.
        # GOOD ENOUGH TO PARSE MY EAGLE FILE AND GET A RESULT FOR NOW...

        # NEED TO MERGE SWITCHER OF BODY + HEADER.
        # DEPENDS ON IF CHANGES TO RULES CAN BE MADE IN PROGRESS.
        # I THINK CHANGES can be made mid file..
        header_switcher = {
            "%": self.toggle_run,  # STOP
            "m95": self.toggle_run,  # STOP
            ";": self.do_nothing,  # COMMENTS
            "inch": lambda: self.update_units(1),  # INCHES
            "metric": lambda: self.update_units(0),  # METRIC
            "ici": self.update_ici,  # CHECK IF RELATIVE OR DIRECT
            "fmat": self.update_fmat,  # UPDATE FORMAT
            "t": self.update_drill_tools  # GENERATES A DRILL TYPE AND SIZE
        }
        # SWITCHER OF EXCELLON BODY SYNTAX OPTIONS.
        body_switcher = {
            ";": self.do_nothing,  # COMMENTS
            "g90": lambda: setattr(self, 'position_instruction_type', 0),
            "g91": lambda: setattr(self, 'position_instruction_type', 1),
            "m30": self.toggle_run,  # STOP
            "m71": lambda: self.update_units(0),  # METRIC
            "m72": lambda: self.update_units(1),  # INCHES
            "t": self.update_current_drill,  # SWITCH SIZE
            "x": self.make_hole
        }

        # CHECK FOR HEADER "m48"
        if self.file_by_line_list[self.line].strip() == "m48":
            # Parses Header
            # Reads Lines from M48 to %
            self.line += 1
            self.search_switcher(header_switcher)
        else:
            raise TypeError(f"Excellon File \"{self.filepath}\" Incorrectly Parsed, missing header at top of file")

        # Parses body.
        self.search_switcher(body_switcher)

        # Returns 2 things:
        # tool_list: A list of tool sizes.
        # EX: T1 = .225   tool_list[0]=.225
        # holes: A dict of holes + cords.
        # EX holes{t#}[x][y]
        # return self.drill_tool_diameter, self.holes

    def make_hole(self):
        # Gets drill position in list
        drill_num = int(self.current_drill[1:]) - 1

        # RAW X-Y from LIST
        match = re.match(r"x(\d+)y(\d+)", self.file_by_line_list[self.line])
        x_raw = int(match.group(1))
        y_raw = int(match.group(2))
        # cleans x_raw and y_raw with formating settings.
        x_real = self.interpret_number_format(x_raw, "x")
        y_real = self.interpret_number_format(y_raw, "y")

        drill_radius = self.drill_tool_diameter[drill_num-1] / 2

        for layer in self.active_layer[drill_num-1]:
            type_of_layer = self.layer_type[drill_num-1]
            self.common_form.add_circle(layer, type_of_layer, x_real, y_real, drill_radius)

    def update_units(self, unit):
        # Updates Units and also checks for TZ/LZ
        self.unit = unit  # INCH(1), METRIC(0)
        self.check_lz_tz()

    def update_current_drill(self):
        self.current_drill = self.file_by_line_list[self.line]

    def update_drill_tools(self):
        # Creates new tool types in a list
        # T1 = [0], T2 = [1], ETC...
        # Diameter is stored inside the list.

        # Gets tool #
        tool_number = int(self.file_by_line_list[self.line][1])
        # Removes the "T#C", gets only the diameter
        tool_diameter = self.file_by_line_list[self.line][3:]

        # Prevents error-ing of index out of rage by init-ing the drill_tool list to be of proper length.
        while len(self.drill_tool_diameter) <= tool_number - 1:
            self.drill_tool_diameter.append(None)

        # Drill tool #1 with a diameter of X,   is in drill_tool_diameter[0] with a value of X
        self.drill_tool_diameter[tool_number - 1] = tool_diameter

    def toggle_run(self):
        self.run = 0

    def check_lz_tz(self):
        if self.file_by_line_list[self.line].find("TZ") != -1:
            # TZ: Trailing Zeros
            self.zero_type = "TZ"
        elif self.file_by_line_list[self.line].find("LZ") != -1:
            # LZ: Leading Zeros
            self.zero_type = "LZ"
        else:
            pass

    def update_ici(self):
        if (self.file_by_line_list[self.line].find("OFF") != -1) or (self.file_by_line_list[self.line].find("0") != -1):
            # ICI = 0
            # STANDARD DIRECT POSITION CORDS
            # EX: X5 means X = 5
            self.position_instruction_type = 0

        elif self.file_by_line_list[self.line].find("1") != -1:
            # ICI = 1
            # RELATIVE POSITION CORDS, RARE
            # EX: X5 means X += 5
            self.position_instruction_type = 1

    def update_fmat(self):
        if self.file_by_line_list[self.line].find("1") != -1:
            # FMAT = 1
            # 1:5 decimal
            # so 012345 becomes
            # 1.2345
            self.number_format = "1:5"
        elif self.file_by_line_list[self.line].find("2") != -1:
            # FMAT = 2
            # 2:4 decimal
            # so 012345 becomes
            # 12.3450
            self.number_format = "2:4"
