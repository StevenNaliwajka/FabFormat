import string


class Infile_Handler():

    # Takes in event??
    def __init__(self, config):
        global boundary, vias, toolpath, xmin, xmax, ymin, ymax
        #
        # read file
        #
        text = infile.get()
        file = open(text, 'r')
        tstr = file.readlines()
        for item in tstr:
            if ((item.find(".cmp") != -1) | (item.find(".sol") != -1) \
                    | (item.find(".otl") != -1)):
                print("reading Gerber file", item)
                boundary = read_Gerber(item)
            elif (item.find(".drl") != -1):
                print("reading Excellon file", item)
                boundary = read_Excellon(tstr)
                vias = read_ExcellonDrill(tstr)
            elif (item.find(".dxf") != -1):
                print("reading DXF file", text)
                boundary = read_DXF(tstr)
            else:
                print("unsupported file type")
                return
            file.close()
        toolpath = []
        sum1 = 0
        for segment in range(len(boundary)):
            sum1 += len(boundary[segment])
            for vertex in range(len(boundary[segment])):
                boundary[segment][vertex][X] += gauss(0, NOISE)
                boundary[segment][vertex][Y] += gauss(0, NOISE)
                x = boundary[segment][vertex][X]
                y = boundary[segment][vertex][Y]
                if (y < ymin): ymin = y
                if (y > ymax): ymax = y
                if (x < xmin): xmin = x
                if (x > xmax): xmax = x
            print(str(segment))
            boundary[segment][-1][X] = boundary[segment][0][X]
            boundary[segment][-1][Y] = boundary[segment][0][Y]
        print("    found", len(boundary), "polygons,", sum1, "vertices")
        print("    added", NOISE, "perturbation")
        print("    xmin: %0.3g " % xmin, "xmax: %0.3g " % xmax, "ymin: %0.3g " % ymin, "ymax: %0.3g " % ymax)
        # FROM WHEN IT TOOK IN EVENT??
        # plot(event)
