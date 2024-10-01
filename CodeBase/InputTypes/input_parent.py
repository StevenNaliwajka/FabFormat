from CodeBase.config import Config
from CodeBase.universal_parent import UniversalParent
from math import *

class InputParent(UniversalParent):
    def __init__(self, ):
        super().__init__()
        self.file_by_list_array = None
        self.path = None

    def read(self):
        # Implemented by child. Parses the read in data.
        pass

    def readfile(self, file_path):
        # Open FIlE + READ IT
        file = open(file_path, 'r')
        tstr = file.readlines()
        file.close()
        self.file_by_list_array = tstr

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