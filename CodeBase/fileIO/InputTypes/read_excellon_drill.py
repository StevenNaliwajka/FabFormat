import re

from CodeBase.fileIO.InputTypes.input_parent import InputParent


# REWRITTEN EXCELLON DRILL PARSER.
# GTG.py's version was lackluster and did not support EAGLE's default .XLN drill file.
# Could be me doing stuff wrong. But its better now.
# I re-wrote to be more legible and flexible.


class ReadExcellonDrill(InputParent):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.readfile(filepath)
        self.file_name = "ReadExcellonDrill"
        self.holes = []

        # Used to store tool sizes.
        # Tool types in a list
        # FORM OF drill_tool_diameter[size][x][y]
        self.drill_tool_diameter = []

        self.current_drill = "T1"  # DEFAULT T1

    def read(self):
        # SWITCHER OF EXCELLON HEADER SYNTAX OPTIONS.
        # IF CONFUSED ON VARS. SEE "universal_parent.py"
        header_switcher = {
            "%": self.toggle_run(),  # STOP
            ";": self.do_nothing(),  # COMMENTS
            "inch": self.update_units(1),  # INCHES
            "metric": self.update_units(0),  # METRIC
            "ici": self.update_ici(),
            "fmat": self.update_fmat(),
            "t": self.update_drill_tools()  #GENERATES DRILL TYPES
        }
        # SWITCHER OF EXCELLON BODY SYNTAX OPTIONS.
        body_switcher = {
            ";": self.do_nothing(),  # COMMENTS
            "m30": self.toggle_run(),  # STOP
            "m71": self.update_units(0),  # METRIC
            "m72": self.update_units(1),  # INCHES
            "t": self.update_current_drill(),  # SWITCH SIZE
            "x": self.make_hole()
        }

        # CHECK FOR HEADER
        if self.file_by_line_list[self.line] == "M48":
            # Parses Header
            # Reads Lines from M48 to %
            self.search_switcher(header_switcher)

        # Parses body. Returns holes,
        self.search_switcher(body_switcher)

        # Returns 2 things:
        # tool_list[]: A list of tool sizes.
        # EX: T1 = .225   tool_list[0]=.225
        # holes[]: A list of holes + cords.
        # EX holes[t#][x][y]
        return self.drill_tool_diameter, self.holes

    def make_hole(self):
        # Gets drill position in list
        drill_num = int(self.current_drill[1:]) - 1

        # RAW X-Y from LIST
        x_raw, y_raw = re.match(r'X(\d+)Y(\d+)', self.file_by_line_list[self.line])
        # cleans x_raw and y_raw with formating settings.
        x_real = self.interpret_number_format(x_raw)
        y_real = self.interpret_number_format(y_raw)

        # Updates with a new hole
        self.holes[drill_num].append([x_real][y_real])

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
        elif self.file_by_line_list[self.line].find("1") != -1:
            # FMAT = 2
            # 2:4 decimal
            # so 012345 becomes
            # 12.3450
            self.number_format = "2:4"
