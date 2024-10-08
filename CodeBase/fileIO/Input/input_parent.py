import re

from CodeBase.fileIO.universal_parent import UniversalParent
from math import *


class InputParent(UniversalParent):
    def __init__(self, ):
        super().__init__()
        self.file_by_line_list = None
        self.path = None
        self.filepath = None

        # Used to stop while loops
        self.run = 0
        # Tracks where in file ya are.
        self.line = 0

        # Exact or relative position instructions
        # 0 (EXACT) is default
        # EXACT EX: X5 means X = 5
        # 1 (RELATIVE) is rare but an option and should be considered if possible
        # RELATIVE EX: X5 means X += 5
        self._position_instruction_type = 0

        # NUMBER FORMATING
        # EX:
        # IF GIVEN A 012345 & MY FORMAT IS 2:4
        # ASSUMING TRAILING ZEROS
        #
        self._number_format = "2:4"

        # ZERO TYPE
        # "TZ" - INCLUDES TRAILING ZEROS (DEFAULT)
        # "LZ" - INCLUDES LEADING ZEROS
        # "AZ" - INCLUDES ALL ZEROS
        # EXAMPLE - 00012345000
        # TZ - 12345000
        # LZ - 00012345
        # AZ - 000123450000
        self._zero_type = "TZ"

    def parse_into_cf(self):
        # Implemented by child. Parses the read in data.
        pass

    def readfile(self, file_path):
        # Open FIlE + READ IT
        file = open(file_path, 'r')
        tstr = file.readlines()
        file.close()
        # Make lowercase so K sensitive is not a problem.
        tstr = [line.lower() for line in tstr]
        self.file_by_line_list = tstr

    def coord(self, tstr, digits, fraction):
        #
        # parse Gerber coordinates
        #
        # global gerbx, gerby
        gerbx = None
        gerby = None
        xindex = tstr.find("X")
        yindex = tstr.find("Y")
        index = tstr.find("D")
        if (xindex == -1):
            x = gerbx
            y = int(tstr[(yindex + 1):index]) * (10 ** (-fraction))
        elif (yindex == -1):
            y = gerby
            x = int(tstr[(xindex + 1):index]) * (10 ** (-fraction))
        else:
            x = int(tstr[(xindex + 1):yindex]) * (10 ** (-fraction))
            y = int(tstr[(yindex + 1):index]) * (10 ** (-fraction))
        gerbx = x
        gerby = y
        return [x, y]

    def stroke(self, x0, y0, x1, y1, width):
        #
        # stroke segment with width
        #
        # print ("stroke:",x0,y0,x1,y1,width
        #global NVERTS
        itemp = 0
        dx = x1 - x0
        dy = y1 - y0
        d = sqrt(dx * dx + dy * dy)
        dxpar = dx / d
        dypar = dy / d
        dxperp = dypar
        dyperp = -dxpar
        dx = -dxperp * width / 2.0
        dy = -dyperp * width / 2.0
        angle = pi / (self.NVERTS / 2 - 1.0)
        c = cos(angle)
        s = sin(angle)
        newpath = []
        for i in range(int(self.NVERTS / 2)):  # NVERTS/2):
            newpath.append([x0 + dx, y0 + dy, []])
            [dx, dy] = [c * dx - s * dy, s * dx + c * dy]
        dx = dxperp * width / 2.0
        dy = dyperp * width / 2.0
        for i in range(int(self.NVERTS / 2)):
            newpath.append([x1 + dx, y1 + dy, []])
            [dx, dy] = [c * dx - s * dy, s * dx + c * dy]
        itemp = itemp + 2 * i  # This is only here to turn off the warning that i is not used
        x0 = newpath[0][self.X]
        y0 = newpath[0][self.Y]
        newpath.append([x0, y0, []])
        return newpath

    def search_switcher(self, switcher):
        # Run till "%" is seen.
        self.run = 1
        flag = False
        while self.run:
            flag = False
            line_content = self.file_by_line_list[self.line].strip().lower()
            for item, method in switcher.items():
                # If item exists in the line, call method.
                if line_content.startswith(item):
                    if callable(method):
                        method()
                        #print(f"Line #{self.line} successfully parsed.")
                        self.line += 1
                        flag = True
                        break
                    else:
                        print(f"{self.file_name}: Method for {item} is not callable")
                if flag:
                    break
            if flag:
                continue
            print(f"{self.file_name}: Line \"{self.line + 1}\" file \"{self.filepath}\" is being incorrectly parsed.")
            print(f"ERRORED LINE IS: {self.file_by_line_list[self.line]}")
            self.line += 1

    def do_nothing(self):
        # Typically used for handling comments in files.
        pass

    def interpret_number_format(self, number):
        # Takes in an Int. Converts it to a modified float with
        # _number_format
        # and
        # _zero_type
        # In mind
        if not isinstance(number, int):
            raise ValueError("The number must be an int.")

        before_decimal, after_decimal = map(int, self._number_format.split(':'))
        number_str = str(number)

        # TRIM ZEROS.
        if self._zero_type == "TZ":  # Trim leading zeros
            self._zero_type = self._zero_type.lstrip('0')
        elif self._zero_type == "LZ":  # Trim trailing zeros
            self._zero_type = self._zero_type.rstrip('0')

        # Ensure the string has enough digits by adding zeros if needed
        number_str = number_str.zfill(before_decimal + after_decimal)
        # Insert the decimal point at the correct position
        formatted_value = f"{number_str[:before_decimal]}.{number_str[before_decimal:before_decimal + after_decimal]}"
        return float(formatted_value)

    @property
    def position_instruction_type(self):
        return self._position_instruction_type

    @property
    def zero_type(self):
        return self._zero_type

    @property
    def number_format(self):
        return self._number_format

    @number_format.setter
    def number_format(self, new_value):
        # Checks for a pattern of "#:#" where # is a number.
        pattern = r'^\d+:\d+$'
        if re.match(pattern, new_value):
            _number_format = new_value

    @zero_type.setter
    def zero_type(self, new_value):
        if new_value in ("TZ", "LZ", "AZ"):
            self._zero_type = new_value

    @position_instruction_type.setter
    def position_instruction_type(self, new_value):
        if new_value == 0 or new_value == 1:
            self._position_instruction_type = new_value
        else:
            raise ValueError(f"{self.file_name}: \"position_instruction_type\" must be equal to 0/1.")
