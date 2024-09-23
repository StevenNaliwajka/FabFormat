import tkinter as tk

from CodeBase.HandlerFiles.config_handler import Config_Handler
from CodeBase.InputFileTypes.read_gerber import read_Gerber
from CodeBase.InputFileTypes.read_excellon import read_Excellon
from CodeBase.InputFileTypes.read_excellon import read_ExcellonDrill
from CodeBase.InputFileTypes.read_dxf import read_DXF

class Gui_Handler():
    def __init__(self, CONFIG: Config_Handler):
        # Overveiw for the tkinter (tk) module
        # (For me to remember everytime I come back and forget)
        # tk.StringVar() creates a StringVariable that can be used to create lables on the GUI
        # tk.Label displays on the GUI, if a tk.StringVar() is passed in it is linked.
        #  -This means that if the tk.StringVar() is updated (for example with XXX.set(YYY)), the GUI Label will update.
        # Frames are widgets that help layout buttons/Labels

        # Creates main application window.
        self.root = tk.Tk()
        # Updates title
        self.root.title('cam.py')
        # Binds key to EXIT
        self.root.bind('q', 'exit')

        # Creates StringVar for Infile
        self.GUIinfile = tk.StringVar()

        # Creates StringVar for outfile
        self.GUIoutfile = tk.StringVar()
        '''
        if (CONFIG.get_infile() != None):
            GUIinfile.set(CONFIG.get_infile())
        else:
            GUIinfile.set('')
        if (CONFIG.get_xoff() != None):
            xoff = CONFIG.get_xoff()
            yoff = CONFIG.get_yoff()
        if (CONFIG.get_size() != None):
            size = CONFIG.get_size()
        if (CONFIG.get_size() != None):
            GUIoutfile.set(CONFIG.get_size())
        else:
            GUIoutfile.set('out.rml')
        if (CONFIG.get_undercut() != None):
            undercut = CONFIG.get_undercut()
        '''

        # Links inframe with frame
        inframe = tk.Frame(self.root)
        tk.Label(inframe, text="input file: ").pack(side="left")
        winfile = tk.Entry(inframe, width=20, textvariable=self.GUIinfile)
        winfile.pack(side="left")
        winfile.bind('<Return>', self.read)
        self.ssize = tk.StringVar()
        self.ssize.set(str(CONFIG.get_size()))
        tk.Label(inframe, text=" ").pack(side="left")
        tk.Label(inframe, text="display size:").pack(side="left")
        self.wsize = tk.Entry(inframe, width=10, textvariable=self.ssize)
        self.wsize.pack(side="left")
        self.wsize.bind('<Return>', self.plot)
        tk.Label(inframe, text=" ").pack(side="left")
        self.ivert = tk.IntVar()
        self.wvert = tk.Checkbutton(inframe, text="show vertices", variable=self.ivert)
        self.wvert.pack(side="left")
        # wvert.bind('<tk.ButtonRelease-1>',plot)
        inframe.pack()

        coordframe = tk.Frame(self.root)
        self.sxoff = tk.StringVar()
        self.sxoff.set(str(CONFIG.get_xoff()))
        self.syoff = tk.StringVar()
        self.syoff.set(str(CONFIG.get_yoff()))
        self.sscale = tk.StringVar()
        self.sscale.set(str(CONFIG.get_scale()))
        tk.Label(coordframe, text="x offset:").pack(side="left")
        self.wxoff = tk.Entry(coordframe, width=10, textvariable=self.sxoff)
        self.wxoff.pack(side="left")
        self.wxoff.bind('<Return>', self.plot)
        tk.Label(coordframe, text=" y offset:").pack(side="left")
        self.wyoff = tk.Entry(coordframe, width=10, textvariable=self.syoff)
        self.wyoff.pack(side="left")
        self.wyoff.bind('<Return>', self.plot)
        tk.Label(coordframe, text=" part scale factor:").pack(side="left")
        self.wscale = tk.Entry(coordframe, width=10, textvariable=self.sscale)
        self.wscale.pack(side="left")
        self.wscale.bind('<Return>', self.plot_delete)
        coordframe.pack()

        c = tk.Canvas(self.root, width=CONFIG.get_window(), height=CONFIG.get_window(), background='white')
        c.pack()

        outframe = tk.Frame(self.root)

        Logo = tk.Canvas(outframe, width=26, height=26, background="white")
        Logo.create_oval(2, 2, 8, 8, fill="red", outline="")
        Logo.create_rectangle(11, 2, 17, 8, fill="blue", outline="")
        Logo.create_rectangle(20, 2, 26, 8, fill="blue", outline="")
        Logo.create_rectangle(2, 11, 8, 17, fill="blue", outline="")
        Logo.create_oval(10, 10, 16, 16, fill="red", outline="")
        Logo.create_rectangle(20, 11, 26, 17, fill="blue", outline="")
        Logo.create_rectangle(2, 20, 8, 26, fill="blue", outline="")
        Logo.create_rectangle(11, 20, 17, 26, fill="blue", outline="")
        Logo.create_rectangle(20, 20, 26, 26, fill="blue", outline="")
        Logo.pack(side="left")
        self.status = tk.StringVar()
        namedate = "    cam.py (" + str(CONFIG.get_date()) + ")  "
        self.status.set(namedate)
        tk.Label(outframe, textvariable=self.status).pack(side="left")
        tk.Label(outframe, text="output file: ").pack(side="left")
        self.woutfile = tk.Entry(outframe, width=20, textvariable=self.GUIoutfile)
        self.woutfile.bind('<Return>', self.camselect)
        self.woutfile.pack(side="left")
        tk.Label(outframe, text=" ").pack(side="left")
        tk.Button(outframe, text="quit", command='exit').pack(side="left")
        tk.Label(outframe, text=" ").pack(side="left")
        outframe.pack()

        camframe = tk.Frame(self.root)
        self.unionbtn = tk.Button(camframe, text="union polygons")
        self.unionbtn.bind('<Button-1>', self.union_boundary)
        self.unionbtn.pack(side="left")
        tk.Label(camframe, text=" ").pack(side="left")
        self.contourbtn = tk.Button(camframe, text="contour boundary")
        self.contourbtn.bind('<Button-1>', self.contour_boundary)
        self.contourbtn.pack(side="left")
        tk.Label(camframe, text=" ").pack(side="left")
        rasterbtn = tk.Button(camframe, text="raster interior")
        rasterbtn.bind('<Button-1>', self.raster)
        rasterbtn.pack(side="left")
        tk.Label(camframe, text=" ").pack(side="left")
        writebtn = tk.Button(camframe, text="write toolpath")
        writebtn.bind('<Button-1>', self.write)
        writebtn.pack(side="left")
        camframe.pack()

        toolframe = tk.Frame(self.root)
        tk.Label(toolframe, text="tool diameter: ").pack(side="left")
        self.sdia = tk.StringVar()
        wtooldia = tk.Entry(toolframe, width=10, textvariable=self.sdia)
        wtooldia.pack(side="left")
        wtooldia.bind('<Return>', self.plot_delete)
        tk.Label(toolframe, text=" contour undercut: ").pack(side="left")
        self.sundercut = tk.StringVar()
        wundercut = tk.Entry(toolframe, width=10, textvariable=self.sundercut)
        wundercut.pack(side="left")
        wundercut.bind('<Return>', self.plot_delete)
        tk.Label(toolframe, text=" raster overlap: ").pack(side="left")
        self.soverlap = tk.StringVar()
        woverlap = tk.Entry(toolframe, width=10, textvariable=self.soverlap)
        woverlap.pack(side="left")
        woverlap.bind('<Return>', self.plot_delete)

        millframe = tk.Frame(self.root)
        tk.Label(millframe, text="z up:").pack(side="left")
        self.szup = tk.StringVar()
        tk.Entry(millframe, width=10, textvariable=self.szup).pack(side="left")
        tk.Label(millframe, text=" z down:").pack(side="left")
        self.szdown = tk.StringVar()
        tk.Entry(millframe, width=10, textvariable=self.szdown).pack(side="left")
        tk.Label(millframe, text=" xy speed:").pack(side="left")
        self.sxyvel = tk.StringVar()
        tk.Entry(millframe, width=10, textvariable=self.sxyvel).pack(side="left")
        tk.Label(millframe, text=" z speed:").pack(side="left")
        self.szvel = tk.StringVar()
        tk.Entry(millframe, width=10, textvariable=self.szvel).pack(side="left")

        gframe = tk.Frame(self.root)
        tk.Label(gframe, text="z top:").pack(side="left")
        self.sztop = tk.StringVar()
        tk.Entry(gframe, width=6, textvariable=self.sztop).pack(side="left")
        tk.Label(gframe, text=" z bottom:").pack(side="left")
        self.szbottom = tk.StringVar()
        tk.Entry(gframe, width=6, textvariable=self.szbottom).pack(side="left")
        tk.Label(gframe, text=" feed rate:").pack(side="left")
        self.sfeed = tk.StringVar()
        tk.Entry(gframe, width=6, textvariable=self.sfeed).pack(side="left")
        tk.Label(gframe, text=" spindle speed:").pack(side="left")
        self.sspindle = tk.StringVar()
        tk.Entry(gframe, width=6, textvariable=self.sspindle).pack(side="left")
        tk.Label(gframe, text=" tool:").pack(side="left")
        self.stool = tk.StringVar()
        tk.Entry(gframe, width=3, textvariable=self.stool).pack(side="left")

        cutframe = tk.Frame(self.root)
        tk.Label(cutframe, text="force: ").pack(side="left")
        self.sforce = tk.StringVar()
        tk.Entry(cutframe, width=10, textvariable=self.sforce).pack(side="left")
        tk.Label(cutframe, text=" velocity:").pack(side="left")
        self.svel = tk.StringVar()
        tk.Entry(cutframe, width=10, textvariable=self.svel).pack(side="left")

        laserframe = tk.Frame(self.root)
        tk.Label(laserframe, text="rate: ").pack(side="left")
        self.srate = tk.StringVar()
        tk.Entry(laserframe, width=10, textvariable=self.srate).pack(side="left")
        tk.Label(laserframe, text=" power:").pack(side="left")
        self.spower = tk.StringVar()
        tk.Entry(laserframe, width=10, textvariable=self.spower).pack(side="left")
        tk.Label(laserframe, text=" speed:").pack(side="left")
        self.sspeed = tk.StringVar()
        tk.Entry(laserframe, width=10, textvariable=self.sspeed).pack(side="left")

        imgframe = tk.Frame(self.root)
        tk.Label(imgframe, text="x size (pixels): ").pack(side="left")
        self.sximg = tk.StringVar()
        tk.Entry(imgframe, width=10, textvariable=self.sximg).pack(side="left")
        tk.Label(imgframe, text=" y size (pixels):").pack(side="left")
        self.syimg = tk.StringVar()
        tk.Entry(imgframe, width=10, textvariable=self.syimg).pack(side="left")

        self.camselect(0)

        if (len(GUIinfile.get()) != 0):
            self.read(0)

        self.root.mainloop()

    def plot(self, event, CONFIG : Config_Handler):
        #global boundary, toolpath, ssize, sscale, sxoff, syoff, ivert, c
        #
        # scale and plot boundary and toolpath
        #
        # size = float(ssize.get())
        size = float(CONFIG.get_size())
        # scale = float(sscale.get())
        scale = float(CONFIG.get_scale())
        # xoff = float(sxoff.get())
        xoff = float(CONFIG.get_xoff())
        # yoff = float(syoff.get())
        yoff = float(CONFIG.get_yoff())
        vert = self.ivert.get()
        c.delete("plot_boundary")
        for seg in range(len(boundary)):
            path_plot = []
            for vertex in range(len(boundary[seg])):
                xplot = int((boundary[seg][vertex][X] * scale + xoff) * WINDOW / size)
                path_plot.append(xplot)
                yplot = WINDOW - int((boundary[seg][vertex][Y] * scale + yoff) * WINDOW / size)
                path_plot.append(yplot)
                if (vert == 1):
                    c.create_text(xplot, yplot, text=str(seg) + ':' + str(vertex), tag="plot_boundary")
            c.create_line(path_plot, tag="plot_boundary")
        c.delete("plot_path")
        for seg in range(len(toolpath)):
            path_plot = []
            for vertex in range(len(toolpath[seg])):
                xplot = int((toolpath[seg][vertex][X] * scale + xoff) * WINDOW / size)
                path_plot.append(xplot)
                yplot = WINDOW - int((toolpath[seg][vertex][Y] * scale + yoff) * WINDOW / size)
                path_plot.append(yplot)
                if (vert == 1):
                    c.create_text(xplot, yplot, text=str(seg) + ':' + str(vertex), tag="plot_path")
            c.create_line(path_plot, tag="plot_path", fill="red")

    def plot_seg(event):
        global segplot, ssize, sscale, sxoff, syoff, ivert, c
        #
        # scale and plot segplot and toolpath
        #
        size = float(ssize.get())
        scale = float(sscale.get())
        xoff = float(sxoff.get())
        yoff = float(syoff.get())
        vert = ivert.get()
        c.delete("plot_segment")
        for seg in range(len(segplot)):
            path_plot = []
            for vertex in range(len(segplot[seg])):
                xplot = int((segplot[seg][vertex][X] * scale + xoff) * WINDOW / size)
                path_plot.append(xplot)
                yplot = WINDOW - int((segplot[seg][vertex][Y] * scale + yoff) * WINDOW / size)
                path_plot.append(yplot)
                if (vert == 1):
                    c.create_text(xplot, yplot, text=str(seg) + ':' + str(vertex), tag="plot_segment")
            c.create_line(path_plot, tag="plot_segment", fill='white')
            c.create_line(path_plot, tag="plot_segment", fill='blue')

    def plot_delete(self, event , CONFIG: Config_Handler):
        #global toolpath
        #
        # scale and plot boundary, delete toolpath
        #
        CONFIG.set_toolpath([])
        print("delete")
        self.plot(event)

    def read(self, event, CONFIG: Config_Handler):
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

        self.plot(event)

    def camselect(self, event):
        #global size
        #
        # pack appropriate CAM GUI options based on output file
        #
        #global outfile, soverlap, szup, szdown, sxyvel, szvel, sforce, svel, srate, spower, sspeed, sztop, szbottom, sfeed, sspindle, stool, sximg, syimg
        text = outfile.get()
        if (text.find(".rml") != -1):

            delframes()
            sdia.set("0.015")
            sundercut.set("0.00")
            soverlap.set("0.8")
            toolframe.pack()
            szup.set("0.04")
            szdown.set("-0.015")
            sxyvel.set("2")
            szvel.set("5")
            millframe.pack()
        elif (text.find(".camm") != -1):
            delframes()
            sforce.set("70")
            svel.set("2")
            cutframe.pack()
        elif (text.find(".epi") != -1):
            delframes()
            srate.set("2500")
            spower.set("50")
            sspeed.set("50")
            ssize.set("10")
            laserframe.pack()
            plot(event)
        elif (text.find(".g") != -1):
            delframes()
            sdia.set("0.015")
            sundercut.set("0.00")
            soverlap.set("0.8")
            toolframe.pack()
            sztop.set("1")
            szbottom.set("0")
            sfeed.set("5")
            sspindle.set("5000")
            stool.set("1")
            gframe.pack()
        elif ((text.find(".scad") != -1) | text.find(".scad")):
            delframes()
            sdia.set("0.015")
            sundercut.set("0.01")
            soverlap.set("0.8")
            toolframe.pack()
            sztop.set("1")
            szbottom.set("0")
            sfeed.set("5")
            sspindle.set("5000")
            stool.set("1")
            gframe.pack()
        elif ((text.find(".jpg") != -1) | (text.find(".bmp") != -1)):
            delframes()
            sdia.set("0.015")
            sundercut.set("0.000")
            soverlap.set("0.8")
            toolframe.pack()
            sximg.set("500")
            syimg.set("500")
            imgframe.pack()
        else:
            print("output file format not supported")
        return

    def union_boundary(self, event, CONFIG: Config_Handler):
        #global boundary, intersections
        #
        # union intersecting polygons on boundary
        #
        print("union boundary ...")
        sign = 1
        # boundary = prune(boundary,sign,event)
        CONFIG.set_boundary(new_prune(CONFIG.get_boundary(), sign, event))
        print("    done")
        self.plot(event)

    def new_prune(path, sign, event):
        #
        # new_prune path intersections
        #
        # first find the intersections
        #
        global segplot
        print("    intersecting ...")
        # plot_path(event)
        # raw_input('before intersection')
        [path, intersections, seg_intersections] = add_intersections(path)
        # print ('path:',path)
        # print ('intersections:',intersections)
        # print ('seg_intersections:',seg_intersections)
        # plot_boundary(event)
        # plot_path(event)
        # raw_input('after intersection')
        print("intersected")
        #
        # then copy non-intersecting segments to new path
        #
        newpath = []
        for seg in range(len(seg_intersections)):
            if (seg_intersections[seg] == []):
                newpath.append(path[seg])
        #
        # Check for internal intersections and delete
        #
        for ii in range(len(intersections) - 1):
            [seg0, vert0] = intersections[ii][0]
            [seg1, vert1] = intersections[ii][1]
            point = path[seg0][vert0]
            poly = path[seg1]
            if (point_in_polygon(point, poly, HUGE)):
                intersections[ii] = []
                print("     Intersection " + str(ii) + "inside poly")
            else:
                point = path[seg1][vert1]
                poly = path[seg0]
                if (point_in_polygon(point, poly, HUGE)):
                    intersections[ii] = []
                    print("     Intersection " + str(ii) + "inside poly")
                # end if
            # end else
        # end for
        #
        # finally follow each outer path and remove the intersections as we go
        #
        print("    pruning ...")
        i = 0
        newseg = 0
        for i in range(len(intersections)):
            if (intersections[i] == []):
                #
                # skip null intersections
                #
                i += 1
                continue
            # else:
            #   istart = i
            #   get the segment in the first intersection
            seg = intersections[i][0][SEG]
            vert = intersections[i][0][VERT]
            seg0 = seg
            vert0 = vert
            sega = intersections[i][1][SEG]  # ending segment and vertex
            verta = intersections[i][1][VERT]  # ending segment and vertex
            segplot = []
            segplot.append(path[seg])
            segplot.append(path[sega])
            plot_seg(event)
            status.set("    " + str(i) + ": intersection " + str(i) + "/" + str(len(intersections) - 1) + "  ")
            outframe.update()
            print("    " + str(i) + ": intersection " + str(i) + "/" + str(len(intersections) - 1) + "  ")
            print_intersections(path, intersections, seg)
            intersections[i] = []  # remove this intersection
            vert1 = (vert + 1) % len(path[seg])
            # calculate a point halfway
            point = path[seg][vert]
            point1 = path[seg][vert1]
            point[0] = point[0] + (point1[0] - point[0]) / 2.0
            point[1] = point[1] + (point1[1] - point[1]) / 2.0
            poly = path[sega]
            forward = not point_in_polygon(point, poly, HUGE)
            print("     Go forward? " + str(forward))
            newseg = len(newpath)
            newpath.append([])
            x = path[seg][vert][X]
            y = path[seg][vert][Y]
            vertc = 0
            print("      new vertex = " + str(vert))
            newpath[newseg].append([])
            newpath[newseg][vertc] = [x, y, []]
            vertc += 1
            intersectindex = []  # clear next intersection
            while (intersectindex != i):  # go all the way around the loop
                if (forward):
                    vert = (vert + 1) % len(path[seg])
                else:
                    vert = (vert - 1) % len(path[seg])
                print("      new vertex = " + str(vert))
                intersectindex = path[seg][vert][INTERSECT]
                if (intersectindex == []):
                    x = path[seg][vert][X]
                    y = path[seg][vert][Y]
                    newpath[newseg].append([])
                    newpath[newseg][vertc] = [x, y, []]
                    vertc += 1
                elif (intersectindex == i):
                    # we've come full circle
                    x = path[seg0][vert0][X]
                    y = path[seg0][vert0][Y]
                    newpath[newseg].append([])
                    newpath[newseg][vertc] = [x, y, []]
                    print("Segment complete [" + str(seg0) + "," + str(vert0) + "] \n\n")
                    break
                else:
                    x = path[seg][vert][X]
                    y = path[seg][vert][Y]
                    newpath[newseg].append([])
                    newpath[newseg][vertc] = [x, y, []]
                    vertc += 1
                    # switch to next segment
                    intersection = intersections[intersectindex]
                    if (intersection == []):
                        print("      Intersection erased go on")
                    else:
                        print("     Intersection = " + str(intersectindex))
                        if (intersection[0][0] == seg):
                            [seg, vert] = intersection[1]
                            [sega, verta] = intersection[0]
                        else:
                            [seg, vert] = intersection[0]
                            [sega, verta] = intersection[1]
                        print("    New segment [" + str(seg) + "," + str(vert) + "]  Old segment [" + str(
                            sega) + "," + str(verta) + "]\n")
                        segplot.append(path[sega])
                        plot_seg(event)
                        outframe.update()
                        intersections[intersectindex] = []  # remove this intersection
                        print_intersections(path, intersections, seg)
                        vert1 = (vert + 1) % len(path[seg])
                        # calculate a point halfway
                        point = path[seg][vert]
                        point1 = path[seg][vert1]
                        point[0] = point[0] + (point1[0] - point[0]) / 2.0
                        point[1] = point[1] + (point1[1] - point[1]) / 2.0
                        poly = path[sega]
                        forward = not point_in_polygon(point, poly, HUGE)
                        print("     Go forward? " + str(forward))
                        print("      new vertex = " + str(vert))
                    # end if
                # end if
            # end while
        return newpath

    def write(self, event, CONFIG : Config_Handler):
        #global toolpath, boundary, vias, xmin, xmax, ymin, ymax, gscale
        #
        # write toolpath
        #
        if (CONFIG.get_toolpath() == []):
             CONFIG.set_toolpath(CONFIG.get_boundary())
        texti = self.GUIinfile.get()
        text = self.GUIoutfile.get()
        if (text.find(".rml") != -1):
            write_RML(toolpath)
        elif (text.find(".camm") != -1):
            write_CAMM(toolpath)
        elif (text.find(".epi") != -1):
            write_EPI(toolpath)
        elif (text.find(".g") != -1):
            write_G(toolpath)
        elif ((text.find(".jpg") != -1) | (text.find(".bmp") != -1)):
            write_img(toolpath)
        elif (text.find(".scad") != -1):
            if (texti.find(".drl") != -1):
                write_via_scad(vias)
            elif (texti.find(".otl") != -1):
                write_outline_scad(toolpath)
            else:
                write_scad(toolpath)

        else:
            print("unsupported output file format")
            return
        sxmin = gscale * (xmin + xoff)
        sxmax = gscale * (xmax + xoff)
        symin = gscale * (ymin + yoff)
        symax = gscale * (ymax + yoff)
        print("    xmin: %0.3g " % sxmin, "xmax: %0.3g " % sxmax, "ymin: %0.3g " % symin, "ymax: %0.3g " % symax)