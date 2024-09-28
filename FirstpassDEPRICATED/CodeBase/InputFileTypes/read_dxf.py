def read_DXF(tstr):
    #
    # DXF parser
    #
    segment = -1
    path = []
    xold = []
    yold = []
    line = 0
    nlines = len(tstr)
    polyline = 0
    vertex = 0
    while line < nlines:
        if (tstr[line] == "POLYLINE\n"):
            segment += 1
            polyline = 1
            path.append([])
        elif (tstr[line] == "VERTEX\n"):
            vertex = 1
        elif ((tstr[line] == "10") & (vertex == 1) & (polyline == 1)):
            line += 1
            x = float(tstr[line])
        elif ((tstr[line] == "20") & (vertex == 1) & (polyline == 1)):
            line += 1
            y = float(tstr[line])
            if ((x != xold) | (y != yold)):
                #
                # add to path if not zero-length segment
                #
                path[segment].append([float(x),float(y),[]])
                xold = x
                yold = y
        elif (tstr[line] == "SEQEND\n"):
            polyline = 0
            vertex = 0
        line += 1
    return path