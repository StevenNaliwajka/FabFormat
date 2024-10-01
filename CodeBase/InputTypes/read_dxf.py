from CodeBase.InputTypes.input_parent import InputParent


class ReadDxf(InputParent):
    def __init__(self, filepath):
        super().__init__()
        self.readfile(filepath)

    def read(self):
        #
        # DXF parser
        #

        segment = -1
        path = []
        xold = []
        yold = []
        line = 0
        nlines = len(self.file_by_list_array)
        polyline = 0
        vertex = 0
        while line < nlines:
            if self.file_by_list_array[line] == "POLYLINE\n":
                segment += 1
                polyline = 1
                path.append([])
            elif self.file_by_list_array[line] == "VERTEX\n":
                vertex = 1
            elif (self.file_by_list_array[line] == "10") & (vertex == 1) & (polyline == 1):
                line += 1
                x = float(self.file_by_list_array[line])
            elif (self.file_by_list_array[line] == "20") & (vertex == 1) & (polyline == 1):
                line += 1
                y = float(self.file_by_list_array[line])
                if (x != xold) | (y != yold):
                    #
                    # add to path if not zero-length segment
                    #
                    path[segment].append([float(x), float(y), []])
                    xold = x
                    yold = y
            elif self.file_by_list_array[line] == "SEQEND\n":
                polyline = 0
                vertex = 0
            line += 1
        return path
