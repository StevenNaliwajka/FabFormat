import tkinter as tk

from CodeBase.DataStructure.config_data import Config_Data
from CodeBase.DataStructure.gui_data import GUI_Data
from CodeBase.InputFileTypes.read_gerber import read_Gerber
from CodeBase.InputFileTypes.read_excellon import read_Excellon
from CodeBase.InputFileTypes.read_excellon import read_ExcellonDrill
from CodeBase.InputFileTypes.read_dxf import read_DXF
from CodeBase.OutputFileTypes.write_g import write_G
from functools import partial


class Gui_Handler():
    def __init__(self, CONFIG: Config_Data,GUI:GUI_Data):
        # Overveiw for the tkinter (tk) module
        # (For me to remember everytime I come back and forget)
        # tk.StringVar() creates a StringVariable that can be used to create lables on the GUI
        # tk.Label displays on the GUI, if a tk.StringVar() is passed in it is linked.
        #  -This means that if the tk.StringVar() is updated (for example with XXX.set(YYY)), the GUI Label will update.
        # Frames are widgets that help layout buttons/Labels

        # Creates main application window.


        # Updates title
        GUI.root().title('cam.py')
        # Binds key to EXIT
        GUI.root().bind('q', 'exit')

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
        GUI.inframe = tk.Frame(GUI.root)
        tk.Label(GUI.inframe, text="input file: ").pack(side="left")
        GUI.winfile = tk.Entry(GUI.inframe, width=20, textvariable=GUI.guiinfile)
        GUI.winfile.pack(side="left")
        GUI.winfile.bind('<Return>', partial(self.read, CONFIG=CONFIG))

        GUI.ssize.set(str(CONFIG.size))
        tk.Label(GUI.inframe, text=" ").pack(side="left")
        tk.Label(GUI.inframe, text="display size:").pack(side="left")
        GUI.wsize = tk.Entry(GUI.inframe, width=10, textvariable=GUI.ssize)
        GUI.wsize.pack(side="left")
        GUI.wsize.bind('<Return>', partial(self.plot, CONFIG=CONFIG))
        tk.Label(GUI.inframe, text=" ").pack(side="left")
        GUI.wvert = tk.Checkbutton(GUI.inframe, text="show vertices", variable=GUI.ivert)
        GUI.wvert.pack(side="left")
        #commented out in cam1
        #GUI.get_wvert.bind('<tk.ButtonRelease-1>',plot)
        GUI.inframe.pack()

        GUI.coordframe = tk.Frame(GUI.root)
        GUI.sxoff.set(str(CONFIG.xoff))
        GUI.syoff.set(str(CONFIG.yoff))
        GUI.sscale.set(str(CONFIG.scale))
        tk.Label(GUI.coordframe, text="x offset:").pack(side="left")
        GUI.wxoff = tk.Entry(GUI.coordframe, width=10, textvariable=GUI.sxoff)
        GUI.wxoff.pack(side="left")
        GUI.wxoff.bind('<Return>', partial(self.plot, CONFIG=CONFIG))

        tk.Label(GUI.coordframe, text=" y offset:").pack(side="left")
        GUI.wyoff = tk.Entry(GUI.coordframe, width=10, textvariable=GUI.syoff)

        GUI.wyoff.pack(side="left")
        GUI.wyoff.bind('<Return>', partial(self.plot, CONFIG=CONFIG))
        tk.Label(GUI.coordframe, text=" part scale factor:").pack(side="left")
        GUI.wscale = tk.Entry(GUI.coordframe, width=10, textvariable=GUI.sscale)
        GUI.wscale.pack(side="left")
        GUI.wscale.bind('<Return>', partial(self.plot_delete, CONFIG=CONFIG))
        GUI.coordframe.pack()

        GUI.c = tk.Canvas(GUI.root, width=CONFIG.window, height=CONFIG.window, background='white')
        GUI.c.pack()

        GUI.outframe = tk.Frame(GUI.root)

        Logo = tk.Canvas(GUI.outframe, width=26, height=26, background="white")
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
        GUI.namedate = "    cam.py (" + str(CONFIG.date) + ")  "
        GUI.status.set(GUI.namedate)
        tk.Label(GUI.outframe, textvariable=GUI.status).pack(side="left")
        tk.Label(GUI.outframe, text="output file: ").pack(side="left")
        GUI.woutfile = tk.Entry(GUI.outframe, width=20, textvariable=GUI.guioutfile)
        GUI.woutfile.bind('<Return>', partial(self.camselect, CONFIG=CONFIG, GUI=GUI))
        GUI.woutfile.pack(side="left")
        tk.Label(GUI.outframe, text=" ").pack(side="left")
        tk.Button(GUI.outframe, text="quit", command='exit').pack(side="left")
        tk.Label(GUI.outframe, text=" ").pack(side="left")
        GUI.outframe.pack()

        GUI.camframe = tk.Frame(GUI.root)
        GUI.unionbtn = tk.Button(GUI.camframe, text="union polygons")
        GUI.unionbtn.bind('<Button-1>', partial(self.union_boundary, CONFIG=CONFIG))
        GUI.unionbtn.pack(side="left")
        tk.Label(GUI.camframe, text=" ").pack(side="left")
        GUI.contourbtn = tk.Button(GUI.camframe, text="contour boundary")
        GUI.contourbtn.bind('<Button-1>', partial(self.contour_boundary, GUI=GUI))
        GUI.contourbtn.pack(side="left")
        tk.Label(GUI.camframe, text=" ").pack(side="left")
        GUI.rasterbtn = tk.Button(GUI.camframe, text="raster interior")
        GUI.rasterbtn.bind('<Button-1>', GUI.rasterbtn)
        GUI.rasterbtn.pack(side="left")
        tk.Label(GUI.camframe, text=" ").pack(side="left")
        GUI.writebtn = tk.Button(GUI.camframe, text="write toolpath")
        GUI.writebtn.bind('<Button-1>', self.write)
        GUI.writebtn.pack(side="left")
        GUI.camframe.pack()

        GUI.toolframe = tk.Frame(GUI.root)
        tk.Label(GUI.toolframe, text="tool diameter: ").pack(side="left")
        GUI.wtooldia = tk.Entry(GUI.toolframe, width=10, textvariable=GUI.sdia)
        GUI.wtooldia.pack(side="left")
        GUI.wtooldia.bind('<Return>', partial(self.plot_delete, CONFIG=CONFIG))
        tk.Label(GUI.toolframe, text=" contour undercut: ").pack(side="left")
        GUI.wundercut = tk.Entry(GUI.toolframe, width=10, textvariable=GUI.sundercut)
        GUI.wundercut.pack(side="left")
        GUI.wundercut.bind('<Return>', partial(self.plot_delete, CONFIG=CONFIG))
        tk.Label(GUI.toolframe, text=" raster overlap: ").pack(side="left")
        GUI.wolverlap = tk.Entry(GUI.toolframe, width=10, textvariable=GUI.soverlap)
        GUI.wolverlap.pack(side="left")
        GUI.wolverlap.bind('<Return>', partial(self.plot_delete, CONFIG=CONFIG))

        GUI.millframe = tk.Frame(GUI.root)
        tk.Label(GUI.millframe, text="z up:").pack(side="left")
        tk.Entry(GUI.millframe, width=10, textvariable=GUI.szup).pack(side="left")
        tk.Label(GUI.millframe, text=" z down:").pack(side="left")
        tk.Entry(GUI.millframe, width=10, textvariable=GUI.szdown).pack(side="left")
        tk.Label(GUI.millframe, text=" xy speed:").pack(side="left")
        tk.Entry(GUI.millframe, width=10, textvariable=GUI.sxyvel).pack(side="left")
        tk.Label(GUI.millframe, text=" z speed:").pack(side="left")
        tk.Entry(GUI.millframe, width=10, textvariable=GUI.szvel).pack(side="left")

        GUI.gframe = tk.Frame(GUI.root)
        tk.Label(GUI.gframe, text="z top:").pack(side="left")
        tk.Entry(GUI.gframe, width=6, textvariable=GUI.sztop).pack(side="left")
        tk.Label(GUI.gframe, text=" z bottom:").pack(side="left")
        tk.Entry(GUI.gframe, width=6, textvariable=GUI.szbottom).pack(side="left")
        tk.Label(GUI.gframe, text=" feed rate:").pack(side="left")
        tk.Entry(GUI.gframe, width=6, textvariable=GUI.sfeed).pack(side="left")
        tk.Label(GUI.gframe, text=" spindle speed:").pack(side="left")
        tk.Entry(GUI.gframe, width=6, textvariable=GUI.sspindle).pack(side="left")
        tk.Label(GUI.gframe, text=" tool:").pack(side="left")
        tk.Entry(GUI.gframe, width=3, textvariable=GUI.stool).pack(side="left")

        GUI.cutframe = tk.Frame(GUI.root)
        tk.Label(GUI.cutframe, text="force: ").pack(side="left")
        tk.Entry(GUI.cutframe, width=10, textvariable=GUI.sforce).pack(side="left")
        tk.Label(GUI.cutframe, text=" velocity:").pack(side="left")
        tk.Entry(GUI.cutframe, width=10, textvariable=GUI.svel).pack(side="left")

        GUI.laserframe = tk.Frame(GUI.root)
        tk.Label(GUI.laserframe, text="rate: ").pack(side="left")
        tk.Entry(GUI.laserframe, width=10, textvariable=GUI.srate).pack(side="left")
        tk.Label(GUI.laserframe, text=" power:").pack(side="left")
        tk.Entry(GUI.laserframe, width=10, textvariable=GUI.spower).pack(side="left")
        tk.Label(GUI.laserframe, text=" speed:").pack(side="left")
        tk.Entry(GUI.laserframe, width=10, textvariable=GUI.sspeed).pack(side="left")

        GUI.imgframe = tk.Frame(GUI.root)
        tk.Label(GUI.imgframe, text="x size (pixels): ").pack(side="left")
        tk.Entry(GUI.imgframe, width=10, textvariable=GUI.sximg).pack(side="left")
        tk.Label(GUI.imgframe, text=" y size (pixels):").pack(side="left")
        tk.Entry(GUI.imgframe, width=10, textvariable=GUI.syimg).pack(side="left")

        self.camselect(0, CONFIG=CONFIG, GUI=GUI)

        if (len(CONFIG._inputFileList) != 0):
            self.read(0,CONFIG=CONFIG)

        GUI.root.mainloop()

    def displace(self, path, GUI:GUI_Data, CONFIG:Config_Data):
        #
        # displace path inwards by tool radius if negitive
        #
        #global sundercut, sdia
        newpath = []
        GUI.scale = float(sscale.get())
        GUI.undercut = float(GUI.sundercut)
        toolrad = (float(GUI.sdia) / 2.0 - GUI.undercut) / GUI.scale
        for seg in range(len(path)):
            GUI.newpath.append([])
            if (len(path[seg]) > 2):
                for vert1 in range(len(path[seg]) - 1):
                    if (vert1 == 0):
                        vert0 = len(path[seg]) - 2
                    else:
                        vert0 = vert1 - 1
                    vert2 = vert1 + 1
                    x0 = path[seg][vert0][CONFIG.X]
                    x1 = path[seg][vert1][CONFIG.X]
                    x2 = path[seg][vert2][CONFIG.X]
                    y0 = path[seg][vert0][CONFIG.Y]
                    y1 = path[seg][vert1][CONFIG.Y]
                    y2 = path[seg][vert2][CONFIG.Y]
                    [dx, dy] = self.offset(x0, x1, x2, y0, y1, y2, toolrad)
                    if (dx != []):
                        newpath[seg].append([(x1 + dx), (y1 + dy), []])
                        if (vert1 == 0):
                            xo = x1 + dx
                            yo = y1 + dy
                        x0 = newpath[seg][0][CONFIG.X]
                        y0 = newpath[seg][0][CONFIG.Y]
                    elif (len(path[seg]) == 2):
                        x0 = path[seg][0][CONFIG.X]
                        y0 = path[seg][0][CONFIG.Y]
                        x1 = path[seg][1][CONFIG.X]
                        y1 = path[seg][1][CONFIG.Y]
                        x2 = 2 * x1 - x0
                        y2 = 2 * y1 - y0
                        [dx, dy] = self.offset(x0, x1, x2, y0, y1, y2, toolrad)
                newpath[seg].append([xo, yo, []])
                x0 = newpath[seg][0][CONFIG.X]
                y0 = newpath[seg][0][CONFIG.Y]
                newpath[seg].append([x0, y0, []])
            else:
                print("  displace: shouldn't happen")
        return newpath

    def offset(x0, x1, x2, y0, y1, y2, r):
        #
        # calculate offset by r for vertex 1
        #
        dx0 = x1 - x0
        dx1 = x2 - x1
        dy0 = y1 - y0
        dy1 = y2 - y1
        d0 = sqrt(dx0 * dx0 + dy0 * dy0)
        d1 = sqrt(dx1 * dx1 + dy1 * dy1)
        if ((d0 == 0) | (d1 == 0)):
            return [[], []]
        dx0par = dx0 / d0
        dy0par = dy0 / d0
        dx0perp = dy0 / d0
        dy0perp = -dx0 / d0
        dx1perp = dy1 / d1
        dy1perp = -dx1 / d1
        # print ("offset points:",x0,x1,x2,y0,y1,y2
        # print ("offset normals:",dx0perp,dx1perp,dy0perp,dy1perp
        if ((abs(dx0perp * dy1perp - dx1perp * dy0perp) < EPS) | \
                (abs(dy0perp * dx1perp - dy1perp * dx0perp) < EPS)):
            dx = r * dx1perp
            dy = r * dy1perp
            # print ("    offset planar:",dx,dy
        elif ((abs(dx0perp + dx1perp) < EPS) & (abs(dy0perp + dy1perp) < EPS)):
            dx = r * dx0par
            dy = r * dy0par
            # print ("    offset hairpin:",dx,dy
        else:
            dx = r * (dy1perp - dy0perp) / \
                 (dx0perp * dy1perp - dx1perp * dy0perp)
            dy = r * (dx1perp - dx0perp) / \
                 (dy0perp * dx1perp - dy1perp * dx0perp)
            # print ("    offset OK:",dx,dy
        return [dx, dy]

    def contour_boundary(self, event, GUI: GUI_Data,CONFIG: Config_Data):
        #global boundary, toolpath
        #
        # contour boundary to find toolpath
        #
        print("contouring boundary ...")
        undercut = float(GUI.sundercut())
        if (undercut != 0.0):
            print("    undercutting contour by", undercut)
            #
            # displace vertices inward by tool size
            #
            print("    displacing ...")
            toolpath = self.displace(path=CONFIG.boundary(), GUI=GUI)
        else:
            print("     WARNING: no displacement set")
        self.plot(event,CONFIG)
        print('displaced')
        sign = -1

        #COMMENTED in CAM1
        # toolpath = new_prune(toolpath,sign,event)

        self.plot(event, CONFIG)
        print("    done")

    def plot(self, event, CONFIG: Config_Data):
        #global boundary, toolpath, ssize, sscale, sxoff, syoff, ivert, c
        #
        # scale and plot boundary and toolpath
        #
        # size = float(ssize.get())
        size = float(CONFIG.size())
        # scale = float(sscale.get())
        scale = float(CONFIG.scale())
        # xoff = float(sxoff.get())
        xoff = float(CONFIG.xoff())
        # yoff = float(syoff.get())
        yoff = float(CONFIG.yoff())
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

    def plot_delete(self, event, CONFIG: Config_Data):
        #global toolpath
        #
        # scale and plot boundary, delete toolpath
        #
        CONFIG.set_toolpath([])
        print("delete")
        self.plot(event)

    def read(self, event, CONFIG: Config_Data):
        inputFileList = CONFIG.inputFileList()
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
        for segment in range(len(CONFIG.boundary())):
            sum1 += len(CONFIG.boundary()[segment])
            for vertex in range(len(CONFIG.boundary()[segment])):
                CONFIG.boundary()[segment][vertex][CONFIG.X()] += gauss(0, CONFIG.noise())
                CONFIG.boundary()[segment][vertex][CONFIG.Y()] += gauss(0, CONFIG.noise())
                x = CONFIG.boundary()[segment][vertex][CONFIG.X()]
                y = CONFIG.boundary()[segment][vertex][CONFIG.Y()]
                if y < CONFIG.ymin():
                    CONFIG.set_ymin(y)
                if y > CONFIG.ymax():
                    CONFIG.set_ymax(y)
                if x < CONFIG.xmin():
                    CONFIG.set_xmin(x)
                if x > CONFIG.xmax():
                    CONFIG.set_xmax(x)
            print(str(segment))
            CONFIG.boundary()[segment][-1][CONFIG.X()] = CONFIG.boundary()[segment][0][CONFIG.X()]
            CONFIG.boundary()[segment][-1][CONFIG.Y()] = CONFIG.boundary()[segment][0][CONFIG.Y()]
        print("    found", len(CONFIG.boundary()), "polygons,", sum1, "vertices")
        print("    added", CONFIG.noise(), "perturbation")
        #print(f"    xmin: %0.3g {xmin}xmax: %0.3g {xmax}ymin: %0.3g {ymin}ymax: %0.3g {ymax}")

        self.plot(event)

    def delframes(self, CONFIG:Config_Data):
        #
        # delete all CAM frames
        #
        #global cutframe, imgframe, toolframe, millframe, gframe, laserframe
        cutframe.pack_forget()
        imgframe.pack_forget()
        toolframe.pack_forget()
        millframe.pack_forget()
        gframe.pack_forget()
        laserframe.pack_forget()

    def camselect(self, event, CONFIG:Config_Data, GUI:GUI_Data):
        #global size
        #
        # pack appropriate CAM GUI options based on output file
        #
        #global outfile, soverlap, szup, szdown, sxyvel, szvel, sforce, svel, srate, spower, sspeed, sztop, szbottom, sfeed, sspindle, stool, sximg, syimg
        text = CONFIG.outputType()
        if (text.find(".rml") != -1):

            self.delframes(CONFIG)
            GUI.set_sdia("0.015")
            GUI.set_sundercut("0.00")
            GUI.set_soverlap("0.8")
            GUI._toolframe.pack()
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

    def union_boundary(self, event, CONFIG: Config_Data):
        #global boundary, intersections
        #
        # union intersecting polygons on boundary
        #
        print("union boundary ...")
        sign = 1
        # boundary = prune(boundary,sign,event)
        CONFIG.set_boundary(new_prune(CONFIG.boundary(), sign, event))
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

    def write(self, event, CONFIG: Config_Data):
        #global toolpath, boundary, vias, xmin, xmax, ymin, ymax, gscale
        #
        # write toolpath
        #
        if (CONFIG.toolpath() == []):
            CONFIG.set_toolpath(CONFIG.boundary())
        texti = self.GUIinfile.get()
        # if (text.find(".rml") != -1):
        #     write_RML(toolpath)
        # elif (text.find(".camm") != -1):
        #     write_CAMM(toolpath)
        # elif (text.find(".epi") != -1):
        #     write_EPI(toolpath)
        if (CONFIG.outputType() == "GCODE"):
            #write_G(toolpath)
            write_G(toolpath, CONFIG)
        # elif ((text.find(".jpg") != -1) | (text.find(".bmp") != -1)):
        #     write_img(toolpath)
        # elif (text.find(".scad") != -1):
        #     if (texti.find(".drl") != -1):
        #         write_via_scad(vias)
        #     elif (texti.find(".otl") != -1):
        #         write_outline_scad(toolpath)
        #     else:
        #         write_scad(toolpath)

        else:
            print("unsupported output file format")
            return
        sxmin = gscale * (xmin + xoff)
        sxmax = gscale * (xmax + xoff)
        symin = gscale * (ymin + yoff)
        symax = gscale * (ymax + yoff)
        print("    xmin: %0.3g " % sxmin, "xmax: %0.3g " % sxmax, "ymin: %0.3g " % symin, "ymax: %0.3g " % symax)
