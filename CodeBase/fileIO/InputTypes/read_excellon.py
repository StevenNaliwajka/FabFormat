from math import *

from CodeBase.fileIO.InputTypes.input_parent import InputParent


class ReadExcellon(InputParent):
    def __init__(self, filepath):
        super().__init__()
        self.readfile(filepath)
        self.holes = None

    def read(self):
        boundary = self.read_Excellon()
        vias = self.read_ExcellonDrill()
        return boundary,vias

    def read_Excellon(self):
        #
        # Excellon parser
        #
        escale = 1
        segment = -1
        line = 0
        nlines = len(self.file_by_list_array)
        print(f"HERE: {nlines}")
        path = []
        drills = []
        vias = []
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
                print (self.file_by_list_array[line][index1+1:index2])
                size = float(self.file_by_list_array[line][index1+1:index2])
                drills[drill] = ["C",size]
                print ("    read drill",drill,"size:",size)
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
                print (self.file_by_list_array[line][index1+1:index2])
                size = float(self.file_by_list_array[line][index1+1:index2])
                drills[drill] = ["C",size]
                print ("    read drill",drill,"size:",size)
                line += 1
                continue
            elif ((self.file_by_list_array[line].find("T") != -1) & (self.file_by_list_array[line].find("C") != -1)):
                #
                # alternate drill definition style
                #
                index = self.file_by_list_array[line].find("T")
                index1 = self.file_by_list_array[line].find("C")
                drill = int(self.file_by_list_array[line][1:index1])
                size = float(self.file_by_list_array[line][index1+1:-1])
                drills[drill] = ["C",size]
                print ("    read drill",drill,"size:",size)
                line += 1
                continue
            elif (self.file_by_list_array[line].find("T") == 0):
                #
                # change drill
                #
                index = self.file_by_list_array[line].find('T')
                drill = int(self.file_by_list_array[line][index+1:-1])
                size = drills[drill][self.SIZE]
                line += 1
                continue
            elif (self.file_by_list_array[line].find("M71") == 0):
                #
                # This is in mm so convert everything t0 inch
                #
                escale = 1/25.4
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
                x0 = escale * float(int(self.file_by_list_array[line][index+1:index1])/10000.0)
                y0 = escale * float(int(self.file_by_list_array[line][index1+1:-1])/10000.0)
                line += 1
                size = drills[drill][self.SIZE]
                path.append([])
                segment += 1
                size = drills[drill][self.SIZE]
                for i in range(self.NVERTS):
                    angle = -i*2.0*pi/(self.NVERTS-1.0)
                    x = x0 + (size/2.0)*cos(angle)
                    y = y0 + (size/2.0)*sin(angle)
                    path[segment].append([x,y,[]])
                continue
            else:
                print ("    not parsed:",self.file_by_list_array[line])
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
                print (self.file_by_list_array[line][index1+1:index2])
                size = float(self.file_by_list_array[line][index1+1:index2])
                drills[drill] = ["C",size]
                print ("    read drill",drill,"size:",size)
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
                print (self.file_by_list_array[line][index1+1:index2])
                size = float(self.file_by_list_array[line][index1+1:index2])
                drills[drill] = ["C",size]
                print ("    read drill",drill,"size:",size)
                line += 1
                continue
            elif ((self.file_by_list_array[line].find("T") != -1) & (self.file_by_list_array[line].find("C") != -1)):
                #
                # alternate drill definition style
                #
                index = self.file_by_list_array[line].find("T")
                index1 = self.file_by_list_array[line].find("C")
                drill = int(self.file_by_list_array[line][1:index1])
                size = float(self.file_by_list_array[line][index1+1:-1])
                drills[drill] = ["C",size]
                print ("    read drill",drill,"size:",size)
                line += 1
                continue
            elif (self.file_by_list_array[line].find("T") == 0):
                #
                # change drill
                #
                index = self.file_by_list_array[line].find('T')
                drill = int(self.file_by_list_array[line][index+1:-1])
                size = drills[drill][self.SIZE]
                line += 1
                continue
            elif (self.file_by_list_array[line].find("M71") == 0):
                #
                # This is in mm so convert everything t0 inch
                #
                escale = 1/25.4
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
                x0 = escale * float(int(self.file_by_list_array[line][index+1:index1])/10000.0)
                y0 = escale * float(int(self.file_by_list_array[line][index1+1:-1])/10000.0)
                line += 1
                size = drills[drill][self.SIZE]
                segment += 1
                holes.append([])
                holes[segment].append([x0,y0,size])
                continue
            else:
                print ("    not parsed:",self.file_by_list_array[line])
            line += 1
        return holes