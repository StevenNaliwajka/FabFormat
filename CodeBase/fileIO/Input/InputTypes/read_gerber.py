from CodeBase.fileIO.Input.input_parent import InputParent
from CodeBase.fileIO.CommonFormat.CFLayer.additive_cf import AdditiveCF
from CodeBase.misc.config import Config


# REWRITING GERBER PARSER TO ALIGN MORE WITH THE UFF (UNIVERSAL FORMAT)
# USING https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf
# AS A BIBLE. PG 19 is helpfull, pg 78 for arcs
# No need to reinvent the wheel till its time; It's time.

class ReadGerber(InputParent):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.readfile(filepath)
        self.file_name = "ReadExcellonDrill"
        self.common_form = AdditiveCF()

        # FLAGS
        self._arc_quad_mode = 0  # FLAG. Can be 0 (0-90°), or 1 (0-360°), Specifies how far an arc can turn.
        self._conv_from_polar = 0  # FLAG. set 1 if LP command, must convert cordinates to cartesian(linear) from polar.
                ## ^ WILL BE A FLAG INSIDE OF THE "%FS" Method..... NOT GLOBAL. SET EACH TIME.
        self._current_infill = 0 # FLAG. set 1 if infil of polygon/circle. 0 if empty.
        self._current_tool = None  # "D10" and higher. Used when loading lines into CF. Updated by "D#" Command.
        self._current_line_type = 1  # 1 = "G01":LINEAR, 2 = "G02":Clockwise, 3 = "G03":CounterClockwise.

        ## NOT SURE HOW APERTURE SELECTION CODE "AM" WORK WITH CF. MAYBE AM CREATES COMMON FORM REGULAR TRACES




    def parse_into_cf(self, CONFIG: Config):
        # NEW GERBER PARSER. INPUTS TRACES BY LINE INTO common_form object

        gerber_switcher = {
            "g04": self.do_nothing(),  # COMMENT
            "g74": lambda: setattr(self, 'arc_quad_mode', 0),  # SINGLE QUAD MODE. ARCS 0-90
            "g75": lambda: setattr(self, 'arc_quad_mode', 1),  # MULTI QUAD MODE ARCS 0-360
            "%momm*%": lambda: setattr(self, 'unit', 0),  # METRIC
            "%moin*%": lambda: setattr(self, 'unit', 1),  # INCH
            "%fs": xxx,  # SPECIFIES (LA/LP/IN) AND XY INT:DECIMAL PRECISION **REQ TO CONV TO LA
            "%lpd%": lambda: setattr(self, 'current_infill', 1),  # POLYGONS/CIRCLES FILL INSIDE
            "%lpc%": lambda: setattr(self, 'current_infill', 0),  # POLYGONS/CIRCLES DONT FILL INSIDE
            "%in": self.do_nothing(),  # SETS FILE NAME, CONSIDERED A COMMENT
            "%ippos*%": lambda: setattr(self, 'current_infill', 1),  # DEPRECATED BUT APPEARS THE SAME TO %LPD%, IN EAGLE FILES.
            "%ipneg*%": lambda: setattr(self, 'current_infill', 0),  # DEPRECATED BUT APPEARS THE SAME TO %LPC%, IN EAGLE FILES.
            "%ad": xxx,  # Creates a template based aperture, assigns D code to it.
            "%am": xxx,  # BEGINS CREATION OF AN APERTURE MACRO.
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

    def create_aperture(self):
        # CREATES A COMMON FORM TOOLHEAD.
        self.common_form.

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
        if new_value in (0,1):
            self._conv_from_polar = new_value

    @arc_quad_mode.setter
    def arc_quad_mode(self, new_value):
        if new_value in (0,1):
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

        '''
        segment = -1
        xold = []
        yold = []
        line = 0
        nlines = len(self.file_by_line_list)
        path = []
        apertures = []
        macros = []
        N_macros = 0
        for i in range(1000):
            apertures.append([])

        for line in self.file_by_line_list:
            if (line.find("%fs") != -1):
                #
                # format statement
                #
                index = line.find("x")
                digits = int(line[index + 1])
                fraction = int(line[index + 2])
                continue
            elif (line.find("%am") != -1):
                #
                # aperture macro
                #
                index = line.find("%am")
                index1 = line.find("*")
                macros.append([])
                macros[-1] = line[index + 3:index1]
                N_macros += 1
                continue
            elif (line.find("%add") != -1):
                #
                # aperture definition
                #
                index = line.find("%add")
                parse = 0
                if (line.find("c,") != -1):
                    #
                    # circle
                    #
                    index = line.find("c,")
                    index1 = line.find("*")
                    aperture = int(line[4:index])
                    size = float(line[index + 2:index1])
                    apertures[aperture] = ["c", size]
                    print("    read aperture", aperture, ": circle diameter", size)

                    continue
                elif (line.find("O,") != -1):
                    #
                    # obround
                    #
                    index = line.find("O,")
                    aperture = int(line[4:index])
                    index1 = line.find(",", index)
                    index2 = line.find("x", index)
                    index3 = line.find("*", index)
                    width = float(line[index1 + 1:index2])
                    height = float(line[index2 + 1:index3])
                    apertures[aperture] = ["O", width, height]
                    print("    read aperture", aperture, ": obround", width, "x", height)

                    continue
                elif (line.find("r,") != -1):
                    #
                    # rectangle
                    #
                    index = line.find("r,")
                    aperture = int(line[4:index])
                    index1 = line.find(",", index)
                    index2 = line.find("x", index)
                    index3 = line.find("*", index)
                    width = float(line[index1 + 1:index2])
                    height = float(line[index2 + 1:index3])
                    apertures[aperture] = ["r", width, height]
                    print("    read aperture", aperture, ": rectangle", width, "x", height)

                    continue
                for macro in range(N_macros):
                    #
                    # macros
                    #
                    index = line.find(macros[macro] + ',')
                    if (index != -1):
                        #
                        # hack: assume macros can be approximated by
                        # a circle, and has a size parameter
                        #
                        aperture = int(line[4:index])
                        index1 = line.find(",", index)
                        index2 = line.find("*", index)
                        size = float(line[index1 + 1:index2])
                        apertures[aperture] = ["c", size]
                        print("    read aperture", aperture, ": macro (assuming circle) diameter", size)
                        parse = 1
                        continue
                if (parse == 0):
                    print("    aperture not implemented:", line)
                    return
            elif (line.find("d") == 0):
                #
                # change aperture
                #
                index = line.find('*')
                aperture = int(line[1:index])
                size = apertures[aperture][self.SIZE]

                continue
            elif (line.find("g54d") == 0):
                #
                # change aperture
                #
                index = line.find('*')
                aperture = int(line[4:index])
                size = apertures[aperture][self.SIZE]

                continue
            elif (line.find("d01*") != -1):
                #
                # pen down
                #
                [xnew, ynew] = self.coord(line, digits, fraction)

                if (size > self.EPS):
                    if ((abs(xnew - xold) > self.EPS) | (abs(ynew - yold) > self.EPS)):
                        newpath = self.stroke(xold, yold, xnew, ynew, size)
                        path.append(newpath)
                        segment += 1
                else:
                    path[segment].append([xnew, ynew, []])
                xold = xnew
                yold = ynew
                continue
            elif (line.find("d02*") != -1):
                #
                # pen up
                #
                [xold, yold] = self.coord(line, digits, fraction)
                if (size < self.EPS):
                    path.append([])
                    segment += 1
                    path[segment].append([xold, yold, []])
                newpath = []

                continue
            elif (line.find("d03*") != -1):
                #
                # flash
                #
                [xnew, ynew] = self.coord(line, digits, fraction)

                if (apertures[aperture][self.TYPE] == "c"):
                    #
                    # circle
                    #
                    path.append([])
                    segment += 1
                    size = apertures[aperture][self.SIZE]
                    for i in range(self.NVERTS):
                        angle = i * 2.0 * pi / (self.NVERTS - 1.0)
                        x = xnew + (size / 2.0) * cos(angle)
                        y = ynew + (size / 2.0) * sin(angle)
                        path[segment].append([x, y, []])
                elif (apertures[aperture][self.TYPE] == "r"):
                    #
                    # rectangle
                    #
                    path.append([])
                    segment += 1
                    width = apertures[aperture][self.WIDTH] / 2.0
                    height = apertures[aperture][self.HEIGHT] / 2.0
                    path[segment].append([xnew - width, ynew - height, []])
                    path[segment].append([xnew + width, ynew - height, []])
                    path[segment].append([xnew + width, ynew + height, []])
                    path[segment].append([xnew - width, ynew + height, []])
                    path[segment].append([xnew - width, ynew - height, []])
                elif (apertures[aperture][self.TYPE] == "O"):
                    #
                    # obround
                    #
                    path.append([])
                    segment += 1
                    width = apertures[aperture][self.WIDTH]
                    height = apertures[aperture][self.HEIGHT]
                    if (width > height):
                        for i in range(self.NVERTS / 2):
                            angle = i * pi / (self.NVERTS / 2 - 1.0) + pi / 2.0
                            x = xnew - (width - height) / 2.0 + (height / 2.0) * cos(angle)
                            y = ynew + (height / 2.0) * sin(angle)
                            path[segment].append([x, y, []])
                        for i in range(self.NVERTS / 2):
                            angle = i * pi / (self.NVERTS / 2 - 1.0) - pi / 2.0
                            x = xnew + (width - height) / 2.0 + (height / 2.0) * cos(angle)
                            y = ynew + (height / 2.0) * sin(angle)
                            path[segment].append([x, y, []])
                    else:
                        for i in range(self.NVERTS / 2):
                            angle = i * pi / (self.NVERTS / 2 - 1.0) + pi
                            x = xnew + (width / 2.0) * cos(angle)
                            y = ynew - (height - width) / 2.0 + (width / 2.0) * sin(angle)
                            path[segment].append([x, y, []])
                        for i in range(self.NVERTS / 2):
                            angle = i * pi / (self.NVERTS / 2 - 1.0)
                            x = xnew + (width / 2.0) * cos(angle)
                            y = ynew + (height - width) / 2.0 + (width / 2.0) * sin(angle)
                            path[segment].append([x, y, []])
                    x = path[segment][-1][self.X]
                    y = path[segment][-1][self.Y]
                    path[segment].append([x, y, []])
                else:
                    print("    aperture", apertures[aperture][self.TYPE], "is not implemented")
                    return
                xold = xnew
                yold = ynew
                continue
            else:
                print("    not parsed:", line)

        return path
        '''
