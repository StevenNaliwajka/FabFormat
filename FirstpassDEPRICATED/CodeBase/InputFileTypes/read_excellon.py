def read_Excellon(tstr):
    #
    # Excellon parser
    #

    escale = 1
    segment = -1
    line = 0
    nlines = len(tstr.readlines())
    print(f"HERE: {nlines}")
    path = []
    drills = []
    vias = []
    #header = tk.TRUE
    for i in range(1000):
        drills.append([])
    while line < nlines:
        if ((tstr[line].find("T") != -1) & (tstr[line].find("C") != -1) \
            & (tstr[line].find("F") != -1)):
            #
            # alternate drill definition style
            #
            index = tstr[line].find("T")
            index1 = tstr[line].find("C")
            index2 = tstr[line].find("F")
            drill = int(tstr[line][1:index1])
            print (tstr[line][index1+1:index2])
            size = float(tstr[line][index1+1:index2])
            drills[drill] = ["C",size]
            print ("    read drill",drill,"size:",size)
            line += 1
            continue
        if ((tstr[line].find("T") != -1) & (tstr[line].find(" ") != -1) \
            & (tstr[line].find("in") != -1)):
            #
            # alternate drill definition style
            #
            index = tstr[line].find("T")
            index1 = tstr[line].find(" ")
            index2 = tstr[line].find("in")
            drill = int(tstr[line][1:index1])
            print (tstr[line][index1+1:index2])
            size = float(tstr[line][index1+1:index2])
            drills[drill] = ["C",size]
            print ("    read drill",drill,"size:",size)
            line += 1
            continue
        elif ((tstr[line].find("T") != -1) & (tstr[line].find("C") != -1)):
            #
            # alternate drill definition style
            #
            index = tstr[line].find("T")
            index1 = tstr[line].find("C")
            drill = int(tstr[line][1:index1])
            size = float(tstr[line][index1+1:-1])
            drills[drill] = ["C",size]
            print ("    read drill",drill,"size:",size)
            line += 1
            continue
        elif (tstr[line].find("T") == 0):
            #
            # change drill
            #
            index = tstr[line].find('T')
            drill = int(tstr[line][index+1:-1])
            size = drills[drill][SIZE]
            line += 1
            continue
        elif (tstr[line].find("M71") == 0):
            #
            # This is in mm so convert everything t0 inch
            #
            escale = 1/25.4
        elif (tstr[line].find("M72") == 0):
            #
            # leave it in inces
            #
            escale = 1
        elif (tstr[line].find("X") != -1):
            #
            # drill location
            #
            index = tstr[line].find("X")
            index1 = tstr[line].find("Y")
            x0 = escale * float(int(tstr[line][index+1:index1])/10000.0)
            y0 = escale * float(int(tstr[line][index1+1:-1])/10000.0)
            line += 1
            size = drills[drill][SIZE]
            path.append([])
            segment += 1 
            size = drills[drill][SIZE]
            for i in range(NVERTS):
                angle = -i*2.0*pi/(NVERTS-1.0)
                x = x0 + (size/2.0)*cos(angle)
                y = y0 + (size/2.0)*sin(angle)
                path[segment].append([x,y,[]])
            continue
        else:
            print ("    not parsed:",tstr[line])
        line += 1
    return path

def read_ExcellonDrill(tstr):
    #
    # Excellon parser
    #
    escale = 1
    segment = -1
    line = 0
    nlines = len(tstr)
    path = []
    drills = []
    holes = []
    #header = tk.TRUE
    for i in range(1000):
        drills.append([])
    while line < nlines:
        if ((tstr[line].find("T") != -1) & (tstr[line].find("C") != -1) \
            & (tstr[line].find("F") != -1)):
            #
            # alternate drill definition style
            #
            index = tstr[line].find("T")
            index1 = tstr[line].find("C")
            index2 = tstr[line].find("F")
            drill = int(tstr[line][1:index1])
            print (tstr[line][index1+1:index2])
            size = float(tstr[line][index1+1:index2])
            drills[drill] = ["C",size]
            print ("    read drill",drill,"size:",size)
            line += 1
            continue
        if ((tstr[line].find("T") != -1) & (tstr[line].find(" ") != -1) \
            & (tstr[line].find("in") != -1)):
            #
            # alternate drill definition style
            #
            index = tstr[line].find("T")
            index1 = tstr[line].find(" ")
            index2 = tstr[line].find("in")
            drill = int(tstr[line][1:index1])
            print (tstr[line][index1+1:index2])
            size = float(tstr[line][index1+1:index2])
            drills[drill] = ["C",size]
            print ("    read drill",drill,"size:",size)
            line += 1
            continue
        elif ((tstr[line].find("T") != -1) & (tstr[line].find("C") != -1)):
            #
            # alternate drill definition style
            #
            index = tstr[line].find("T")
            index1 = tstr[line].find("C")
            drill = int(tstr[line][1:index1])
            size = float(tstr[line][index1+1:-1])
            drills[drill] = ["C",size]
            print ("    read drill",drill,"size:",size)
            line += 1
            continue
        elif (tstr[line].find("T") == 0):
            #
            # change drill
            #
            index = tstr[line].find('T')
            drill = int(tstr[line][index+1:-1])
            size = drills[drill][SIZE]
            line += 1
            continue
        elif (tstr[line].find("M71") == 0):
            #
            # This is in mm so convert everything t0 inch
            #
            escale = 1/25.4
        elif (tstr[line].find("M72") == 0):
            #
            # leave it in inces
            #
            escale = 1
        elif (tstr[line].find("X") != -1):
            #
            # drill location
            #
            index = tstr[line].find("X")
            index1 = tstr[line].find("Y")
            x0 = escale * float(int(tstr[line][index+1:index1])/10000.0)
            y0 = escale * float(int(tstr[line][index1+1:-1])/10000.0)
            line += 1
            size = drills[drill][SIZE]
            segment += 1
            holes.append([])
            holes[segment].append([x0,y0,size])
            continue
        else:
            print ("    not parsed:",tstr[line])
        line += 1
    return holes