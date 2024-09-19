import os

from CodeBase.HandlerFiles.config_handler import Config_Handler


def read_Gerber(fileName, CONFIG: Config_Handler):
    #
    # Gerber parser
    #
    #
    input_file_path = os.path.join(CONFIG.get_infileDirectoryPath(), fileName)


    segment = -1
    xold = []
    yold = []
    line = 0
    #nlines = len(tstr)
    #print(f"HERE: {nlines}")
    path = []
    apertures = []
    macros = []
    N_macros = 0
    for i in range(1000):
        apertures.append([])
    #while line < nlines:
    with open(input_file_path, 'r') as file:
        for line in file:
            if (line.find("%FS") != -1):
                #
                # format statement
                #
                index = line.find("X")
                digits = int(line[index + 1])
                fraction = int(line[index + 2])
                continue
            elif (line.find("%AM") != -1):
                #
                # aperture macro
                #
                index = line.find("%AM")
                index1 = line.find("*")
                macros.append([])
                macros[-1] = line[index + 3:index1]
                N_macros += 1
                continue
            elif (line.find("%ADD") != -1):
                #
                # aperture definition
                #
                index = line.find("%ADD")
                parse = 0
                if (line.find("C,") != -1):
                    #
                    # circle
                    #
                    index = line.find("C,")
                    index1 = line.find("*")
                    aperture = int(line[4:index])
                    size = float(line[index + 2:index1])
                    apertures[aperture] = ["C", size]
                    print("    read aperture", aperture, ": circle diameter", size)

                    continue
                elif (line.find("O,") != -1):
                    #
                    # obround
                    #
                    index = line.find("O,")
                    aperture = int(line[4:index])
                    index1 = line.find(",", index)
                    index2 = line.find("X", index)
                    index3 = line.find("*", index)
                    width = float(line[index1 + 1:index2])
                    height = float(line[index2 + 1:index3])
                    apertures[aperture] = ["O", width, height]
                    print("    read aperture", aperture, ": obround", width, "x", height)

                    continue
                elif (line.find("R,") != -1):
                    #
                    # rectangle
                    #
                    index = line.find("R,")
                    aperture = int(line[4:index])
                    index1 = line.find(",", index)
                    index2 = line.find("X", index)
                    index3 = line.find("*", index)
                    width = float(line[index1 + 1:index2])
                    height = float(line[index2 + 1:index3])
                    apertures[aperture] = ["R", width, height]
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
                        apertures[aperture] = ["C", size]
                        print("    read aperture", aperture, ": macro (assuming circle) diameter", size)
                        parse = 1
                        continue
                if (parse == 0):
                    print("    aperture not implemented:", line)
                    return
            elif (line.find("D") == 0):
                #
                # change aperture
                #
                index = line.find('*')
                aperture = int(line[1:index])
                size = apertures[aperture][CONFIG.get_size()]

                continue
            elif (line.find("G54D") == 0):
                #
                # change aperture
                #
                index = line.find('*')
                aperture = int(line[4:index])
                size = apertures[aperture][CONFIG.get_size()]

                continue
            elif (line.find("D01*") != -1):
                #
                # pen down
                #
                [xnew, ynew] = coord(line, digits, fraction)

                if (size > EPS):
                    if ((abs(xnew - xold) > EPS) | (abs(ynew - yold) > EPS)):
                        newpath = stroke(xold, yold, xnew, ynew, size)
                        path.append(newpath)
                        segment += 1
                else:
                    path[segment].append([xnew, ynew, []])
                xold = xnew
                yold = ynew
                continue
            elif (line.find("D02*") != -1):
                #
                # pen up
                #
                [xold, yold] = coord(line, digits, fraction)
                if (size < EPS):
                    path.append([])
                    segment += 1
                    path[segment].append([xold, yold, []])
                newpath = []

                continue
            elif (line.find("D03*") != -1):
                #
                # flash
                #
                [xnew, ynew] = coord(line, digits, fraction)

                if (apertures[aperture][TYPE] == "C"):
                    #
                    # circle
                    #
                    path.append([])
                    segment += 1
                    size = apertures[aperture][SIZE]
                    for i in range(NVERTS):
                        angle = i * 2.0 * pi / (NVERTS - 1.0)
                        x = xnew + (size / 2.0) * cos(angle)
                        y = ynew + (size / 2.0) * sin(angle)
                        path[segment].append([x, y, []])
                elif (apertures[aperture][TYPE] == "R"):
                    #
                    # rectangle
                    #
                    path.append([])
                    segment += 1
                    width = apertures[aperture][WIDTH] / 2.0
                    height = apertures[aperture][HEIGHT] / 2.0
                    path[segment].append([xnew - width, ynew - height, []])
                    path[segment].append([xnew + width, ynew - height, []])
                    path[segment].append([xnew + width, ynew + height, []])
                    path[segment].append([xnew - width, ynew + height, []])
                    path[segment].append([xnew - width, ynew - height, []])
                elif (apertures[aperture][TYPE] == "O"):
                    #
                    # obround
                    #
                    path.append([])
                    segment += 1
                    width = apertures[aperture][WIDTH]
                    height = apertures[aperture][HEIGHT]
                    if (width > height):
                        for i in range(NVERTS / 2):
                            angle = i * pi / (NVERTS / 2 - 1.0) + pi / 2.0
                            x = xnew - (width - height) / 2.0 + (height / 2.0) * cos(angle)
                            y = ynew + (height / 2.0) * sin(angle)
                            path[segment].append([x, y, []])
                        for i in range(NVERTS / 2):
                            angle = i * pi / (NVERTS / 2 - 1.0) - pi / 2.0
                            x = xnew + (width - height) / 2.0 + (height / 2.0) * cos(angle)
                            y = ynew + (height / 2.0) * sin(angle)
                            path[segment].append([x, y, []])
                    else:
                        for i in range(NVERTS / 2):
                            angle = i * pi / (NVERTS / 2 - 1.0) + pi
                            x = xnew + (width / 2.0) * cos(angle)
                            y = ynew - (height - width) / 2.0 + (width / 2.0) * sin(angle)
                            path[segment].append([x, y, []])
                        for i in range(NVERTS / 2):
                            angle = i * pi / (NVERTS / 2 - 1.0)
                            x = xnew + (width / 2.0) * cos(angle)
                            y = ynew + (height - width) / 2.0 + (width / 2.0) * sin(angle)
                            path[segment].append([x, y, []])
                    x = path[segment][-1][X]
                    y = path[segment][-1][Y]
                    path[segment].append([x, y, []])
                else:
                    print("    aperture", apertures[aperture][TYPE], "is not implemented")
                    return
                xold = xnew
                yold = ynew
                continue
            else:
                print("    not parsed:", line)
    return path
