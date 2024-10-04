from math import *

from CodeBase.fileIO.InputTypes.input_parent import InputParent


class ReadExcellon(InputParent):
    def __init__(self, filepath):
        super().__init__()
        self.readfile(filepath)
        self.holes = None

        # Used to store tool sizes.
        self.drill_tool_diameter = []

    def read(self):
        boundary = self.read_Excellon()
        vias = self.read_ExcellonDrill()
        return boundary, vias

    def read_Excellon(self):
        #
        # Excellon parser
        #
        escale = 1
        segment = -1
        line = 0
        nlines = len(self.file_by_list_array)
        #print(f"HERE: {nlines}")
        path = []
        drills = []
        vias = []
        #header = tk.TRUE
        self.drill_tool_diameter = []
        # Stores drill tool diamaters
        for i in range(1000):
            drills.append([])
        while line < nlines:
            if self.file_by_list_array[line][0] == "M48":
                # Parses Header
                # Reads Lines from M48 to %
                line = self.parse_header(line)
                continue
            #print(f"Current Line: {self.file_by_list_array[line][0]}")
            elif self.file_by_list_array[line][0] == ";":
                # MetaData, Comments...
                line += 1
                continue
            if ((self.file_by_list_array[line].find("T") != -1) & (self.file_by_list_array[line].find("C") != -1)
                    & (self.file_by_list_array[line].find("F") != -1)):
                #
                # alternate drill definition style
                #
                index = self.file_by_list_array[line].find("T")
                index1 = self.file_by_list_array[line].find("C")
                index2 = self.file_by_list_array[line].find("F")
                drill = int(self.file_by_list_array[line][1:index1])
                print(self.file_by_list_array[line][index1 + 1:index2])
                size = float(self.file_by_list_array[line][index1 + 1:index2])
                drills[drill] = ["C", size]
                print("    read drill", drill, "size:", size)
                line += 1
                continue
            if ((self.file_by_list_array[line].find("T") != -1) & (self.file_by_list_array[line].find(" ") != -1)
                    & (self.file_by_list_array[line].find("in") != -1)):
                #
                # alternate drill definition style
                #
                index = self.file_by_list_array[line].find("T")
                index1 = self.file_by_list_array[line].find(" ")
                index2 = self.file_by_list_array[line].find("in")
                drill = int(self.file_by_list_array[line][1:index1])
                print(self.file_by_list_array[line][index1 + 1:index2])
                size = float(self.file_by_list_array[line][index1 + 1:index2])
                drills[drill] = ["C", size]
                print("    read drill", drill, "size:", size)
                line += 1
                continue
            elif ((self.file_by_list_array[line].find("T") != -1) & (self.file_by_list_array[line].find("C") != -1)):
                #
                # alternate drill definition style
                #
                index = self.file_by_list_array[line].find("T")
                index1 = self.file_by_list_array[line].find("C")

                # MODIFIED STUFF HERE
                #if self.file_by_list_array[line][1:index1] == '':
                # drill = 0
                #else:
                drill = int(self.file_by_list_array[line][1:index1])
                size = float(self.file_by_list_array[line][index1 + 1:-1])
                drills[drill] = ["C", size]
                print("    read drill", drill, "size:", size)
                line += 1
                continue
            elif (self.file_by_list_array[line].find("T") == 0):
                #
                # change drill
                #
                index = self.file_by_list_array[line].find('T')
                drill = int(self.file_by_list_array[line][index + 1:-1])
                size = drills[drill][self.SIZE]
                line += 1
                continue
            elif (self.file_by_list_array[line].find("M71") == 0):
                #
                # This is in mm so convert everything t0 inch
                #
                escale = 1 / 25.4
            elif (self.file_by_list_array[line].find("M72") == 0):
                #
                # leave it in inces
                #
                escale = 1
            elif (self.file_by_list_array[line].find("X") != -1):
                #
                # drill location
                #
                index = self.file_by_list_array[line].find("X")
                index1 = self.file_by_list_array[line].find("Y")
                x0 = escale * float(int(self.file_by_list_array[line][index + 1:index1]) / 10000.0)
                y0 = escale * float(int(self.file_by_list_array[line][index1 + 1:-1]) / 10000.0)
                line += 1
                size = drills[drill][self.SIZE]
                path.append([])
                segment += 1
                size = drills[drill][self.SIZE]
                for i in range(self.NVERTS):
                    angle = -i * 2.0 * pi / (self.NVERTS - 1.0)
                    x = x0 + (size / 2.0) * cos(angle)
                    y = y0 + (size / 2.0) * sin(angle)
                    path[segment].append([x, y, []])
                continue
            else:
                print("    not parsed:", self.file_by_list_array[line])
            line += 1
        return path

    def read_ExcellonDrill(self):
        #
        # Excellon parser
        #
        escale = 1
        segment = -1
        line = 0
        nlines = len(self.file_by_list_array)
        path = []
        drills = []
        holes = []
        #header = tk.TRUE
        for i in range(1000):
            drills.append([])
        while line < nlines:
            if ((self.file_by_list_array[line].find("T") != -1) & (self.file_by_list_array[line].find("C") != -1) \
                    & (self.file_by_list_array[line].find("F") != -1)):
                #
                # alternate drill definition style
                #
                index = self.file_by_list_array[line].find("T")
                index1 = self.file_by_list_array[line].find("C")
                index2 = self.file_by_list_array[line].find("F")
                drill = int(self.file_by_list_array[line][1:index1])
                print(self.file_by_list_array[line][index1 + 1:index2])
                size = float(self.file_by_list_array[line][index1 + 1:index2])
                drills[drill] = ["C", size]
                print("    read drill", drill, "size:", size)
                line += 1
                continue
            if ((self.file_by_list_array[line].find("T") != -1) & (self.file_by_list_array[line].find(" ") != -1) \
                    & (self.file_by_list_array[line].find("in") != -1)):
                #
                # alternate drill definition style
                #
                index = self.file_by_list_array[line].find("T")
                index1 = self.file_by_list_array[line].find(" ")
                index2 = self.file_by_list_array[line].find("in")
                drill = int(self.file_by_list_array[line][1:index1])
                print(self.file_by_list_array[line][index1 + 1:index2])
                size = float(self.file_by_list_array[line][index1 + 1:index2])
                drills[drill] = ["C", size]
                print("    read drill", drill, "size:", size)
                line += 1
                continue
            elif (self.file_by_list_array[line].find("T") != -1) & (self.file_by_list_array[line].find("C") != -1):
                #
                # alternate drill definition style
                #
                index = self.file_by_list_array[line].find("T")
                index1 = self.file_by_list_array[line].find("C")
                drill = int(self.file_by_list_array[line][1:index1])
                size = float(self.file_by_list_array[line][index1 + 1:-1])
                drills[drill] = ["C", size]
                print("    read drill", drill, "size:", size)
                line += 1
                continue
            elif (self.file_by_list_array[line].find("T") == 0):
                #
                # change drill
                #
                index = self.file_by_list_array[line].find('T')
                drill = int(self.file_by_list_array[line][index + 1:-1])
                size = drills[drill][self.SIZE]
                line += 1
                continue
            elif (self.file_by_list_array[line].find("M71") == 0):
                #
                # This is in mm so convert everything t0 inch
                #
                escale = 1 / 25.4
            elif (self.file_by_list_array[line].find("M72") == 0):
                #
                # leave it in inces
                #
                escale = 1
            elif (self.file_by_list_array[line].find("X") != -1):
                #
                # drill location
                #
                index = self.file_by_list_array[line].find("X")
                index1 = self.file_by_list_array[line].find("Y")
                x0 = escale * float(int(self.file_by_list_array[line][index + 1:index1]) / 10000.0)
                y0 = escale * float(int(self.file_by_list_array[line][index1 + 1:-1]) / 10000.0)
                line += 1
                size = drills[drill][self.SIZE]
                segment += 1
                holes.append([])
                holes[segment].append([x0, y0, size])
                continue
            else:
                print("    not parsed:", self.file_by_list_array[line])
            line += 1
        return holes

    def parse_header(self, line):
        drill_tool_diameter = []
        while self.file_by_list_array[line][0] != "%":
            if self.file_by_list_array[line][0] == ";":
                # MetaData, Comments...
                line += 1
                continue
            elif self.file_by_list_array[line].find("INCH") != -1:
                # UNITS INCH
                if self.file_by_list_array[line].find("TZ") != -1:
                    # TZ
                    pass
                elif self.file_by_list_array[line].find("LZ") != -1:
                    # LZ
                    pass
                line += 1
                continue
            elif self.file_by_list_array[line].find("METRIC") != -1:
                # UNITS MM
                if self.file_by_list_array[line].find("TZ") != -1:
                    # TZ
                    pass
                elif self.file_by_list_array[line].find("LZ") != -1:
                    # LZ
                    pass
                line += 1
                continue
            elif self.file_by_list_array[line].find("ICI") != -1:
                if (self.file_by_list_array[line].find("OFF") != -1) or (self.file_by_list_array[line].find("0") != -1):
                    # ICI = 0
                    pass
                elif self.file_by_list_array[line].find("1") != -1:
                    # ICI = 1
                    pass
                line += 1
                continue
            elif self.file_by_list_array[line].find("FMAT"):
                if self.file_by_list_array[line].find("1") != -1:
                    # FMAT = 1
                    pass
                elif self.file_by_list_array[line].find("1") != -1:
                    # FMAT = 2
                    pass
            elif self.file_by_list_array[line].find("T") != -1:
                # Creates new tool types in a list
                # T1 = [0], T2 = [1], ETC...
                # Diameter is stored inside the list.

                # Gets tool #
                tool_number = int(self.file_by_list_array[line][1])
                # Removes the "T#C", gets only the diameter
                tool_diameter = self.file_by_list_array[line][3:]

                # Drill tool #1 with a diameter of X,   is in drill_tool_diameter[0] with a value of X
                self.drill_tool_diameter[tool_number - 1] = tool_diameter
                line += 1
                continue
            else:
                print(f"Error: Excellion line: \"{self.file_by_list_array[line]}\" is not being parsed; Notify DEV.")
                line += 1
        # Returns position of file after parsing Header is done
        return line
