import string
from CodeBase.HandlerFiles.config_handler import Config_Handler
from CodeBase.InputFileTypes.read_gerber import read_Gerber
from CodeBase.InputFileTypes.read_excellon import read_Excellon
from CodeBase.InputFileTypes.read_excellon import read_ExcellonDrill
from CodeBase.InputFileTypes.read_dxf import read_DXF
from random import gauss


class Infile_Handler():

    # Takes in event??
    def __init__(self, CONFIG: Config_Handler):
        #WAS OG:
        # global boundary, vias, toolpath, xmin, xmax, ymin, ymax
        #UPDATED TO USE CONFIG ALREADY,
        # boundary, vias, toolpath, xmin, xmax, ymin, ymax

        #
        # read file
        #
        text = CONFIG.get_infile()
        file = open(text, 'r')
        tstr = file.readlines()
        for item in tstr:
            if ((item.find(".cmp") != -1) | (item.find(".sol") != -1)
                    | (item.find(".otl") != -1)):
                print("reading Gerber file", item)
                CONFIG.set_boundary(read_Gerber(item, CONFIG))
            elif (item.find(".drl") != -1):
                print("reading Excellon file", item)
                CONFIG.set_boundary(read_Excellon(tstr))
                CONFIG.set_vias(read_ExcellonDrill(tstr))
            elif (item.find(".dxf") != -1):
                print("reading DXF file", text)
                CONFIG.set_boundary(read_DXF(tstr))
            else:
                print("unsupported file type")
                return
            file.close()
        CONFIG.set_toolpath([])
        sum1 = 0
        for segment in range(len(CONFIG.get_boundary())):
            sum1 += len(CONFIG.get_boundary()[segment])
            for vertex in range(len(CONFIG.get_boundary()[segment])):
                CONFIG.get_boundary()[segment][vertex][CONFIG.get_X()] += gauss(0, CONFIG.get_noise())
                CONFIG.get_boundary()[segment][vertex][CONFIG.get_Y()] += gauss(0, CONFIG.get_noise())
                x = CONFIG.get_boundary()[segment][vertex][CONFIG.get_X()]
                y = CONFIG.get_boundary()[segment][vertex][CONFIG.get_Y()]
                if y < CONFIG.get_ymin():
                    CONFIG.set_ymin(y)
                if y > CONFIG.get_ymax():
                    CONFIG.set_ymax(y)
                if x < CONFIG.get_xmin():
                    CONFIG.set_xmin(x)
                if x > CONFIG.get_xmax():
                    CONFIG.set_xmax(x)
            print(str(segment))
            CONFIG.get_boundary()[segment][-1][CONFIG.get_X()] = CONFIG.get_boundary()[segment][0][CONFIG.get_X()]
            CONFIG.get_boundary()[segment][-1][CONFIG.get_Y()] = CONFIG.get_boundary()[segment][0][CONFIG.get_Y()]
        print("    found", len(CONFIG.get_boundary()), "polygons,", sum1, "vertices")
        print("    added", CONFIG.get_noise(), "perturbation")
        #print(f"    xmin: %0.3g {xmin}xmax: %0.3g {xmax}ymin: %0.3g {ymin}ymax: %0.3g {ymax}")
        # FROM WHEN IT TOOK IN EVENT??
        # plot(event)
