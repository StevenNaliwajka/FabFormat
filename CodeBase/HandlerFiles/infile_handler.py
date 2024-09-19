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
        # Navigates through the input file list, determines the file type and parses each as required.
        inputFileList = CONFIG.get_inputFileList()
        for item in inputFileList:
            if ((item.find(".cmp") != -1) | (item.find(".sol") != -1)
                    | (item.find(".otl") != -1)):
                print(f"Infile Handler: Reading Gerber file: {item}")
                CONFIG.set_boundary(read_Gerber(item, CONFIG))
            elif (item.find(".drl") != -1):
                print(f"Infile Handler: Reading Excellon file: {item}")
                CONFIG.set_boundary(read_Excellon(item))
                CONFIG.set_vias(read_ExcellonDrill(item))
            elif (item.find(".dxf") != -1):
                print(f"Infile Handler: Reading DXF file: {item}")
                CONFIG.set_boundary(read_DXF(item))
            else:
                print("unsupported file type")
                return
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
