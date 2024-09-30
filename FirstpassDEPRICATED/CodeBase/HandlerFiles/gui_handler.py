import tkinter as tk
from math import sqrt
from random import gauss
from CodeBase.DataStructure.config_data import Config_Data
from CodeBase.DataStructure.gui_data import GUI_Data
from CodeBase.InputTypes.read_gerber import read_Gerber
from CodeBase.InputTypes.read_excellon import read_Excellon
from CodeBase.InputTypes.read_excellon import read_ExcellonDrill
from CodeBase.InputTypes.read_dxf import read_DXF
from CodeBase.OutputTypes.write_gcode import write_G
from functools import partial


class Gui_Handler():
    def __init__(self, CONFIG: Config_Data, GUI: GUI_Data):
        # Overveiw for the tkinter (tk) module
        # (For me to remember everytime I come back and forget)
        # tk.StringVar() creates a StringVariable that can be used to create lables on the GUI
        # tk.Label displays on the GUI, if a tk.StringVar() is passed in it is linked.
        #  -This means that if the tk.StringVar() is updated (for example with XXX.set(YYY)), the GUI Label will update.
        # Frames are widgets that help layout buttons/Labels

        # Creates main application window.
        self._root = tk.Tk()
        # Updates title
        #GUI.root().title('cam.py')
        self._root.title('cam.py')
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
        # commented out in cam1
        # GUI.get_wvert.bind('<tk.ButtonRelease-1>',plot)
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

        if len(CONFIG.inputFileList) != 0:
            self.read(0, CONFIG=CONFIG)

        GUI.root.mainloop()

    def displace(self, path, GUI: GUI_Data, CONFIG: Config_Data):
        #
        # displace path inwards by tool radius if negitive
        #
        # global sundercut, sdia
        newpath = []
        GUI.scale = float(sscale.get())
        GUI.undercut = float(GUI.sundercut)
        toolrad = (float(GUI.sdia) / 2.0 - GUI.undercut) / GUI.scale
        for seg in range(len(path)):
            GUI.newpath.append([])
            if len(path[seg]) > 2:
                for vert1 in range(len(path[seg]) - 1):
                    if vert1 == 0:
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
                    [dx, dy] = self.offset(x0, x1, x2, y0, y1, y2, toolrad, CONFIG)
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
                        [dx, dy] = self.offset(x0, x1, x2, y0, y1, y2, toolrad, CONFIG)
                newpath[seg].append([xo, yo, []])
                x0 = newpath[seg][0][CONFIG.X]
                y0 = newpath[seg][0][CONFIG.Y]
                newpath[seg].append([x0, y0, []])
            else:
                print("  displace: shouldn't happen")
        return newpath

    def offset(self, x0, x1, x2, y0, y1, y2, r, CONFIG: Config_Data):
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
        if ((abs(dx0perp * dy1perp - dx1perp * dy0perp) < CONFIG.eps) |
                (abs(dy0perp * dx1perp - dy1perp * dx0perp) < CONFIG.eps)):
            dx = r * dx1perp
            dy = r * dy1perp
            # print ("    offset planar:",dx,dy
        elif ((abs(dx0perp + dx1perp) < CONFIG.eps) & (abs(dy0perp + dy1perp) < CONFIG.eps)):
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

    def contour_boundary(self, event, GUI: GUI_Data, CONFIG: Config_Data):
        # global boundary, toolpath
        #
        # contour boundary to find toolpath
        #
        print("contouring boundary ...")
        undercut = float(GUI.sundercut)
        if undercut != 0.0:
            print("    undercutting contour by", undercut)
            #
            # displace vertices inward by tool size
            #
            print("    displacing ...")
            CONFIG.toolpath = self.displace(path=CONFIG.boundary, GUI=GUI)
        else:
            print("     WARNING: no displacement set")
        self.plot(event, CONFIG)
        print('displaced')
        # COMMENTED in CAM1
        # sign = -1
        # toolpath = new_prune(toolpath,sign,event)

        self.plot(event, CONFIG)
        print("    done")

    def plot(self, event, CONFIG: Config_Data, GUI: GUI_Data):
        # global boundary, toolpath, ssize, sscale, sxoff, syoff, ivert, c
        #
        # scale and plot boundary and toolpath
        #
        size = float(CONFIG.size)
        scale = float(CONFIG.scale)
        xoff = float(CONFIG.xoff)
        yoff = float(CONFIG.yoff)
        vert = GUI.ivert.get()
        c.delete("plot_boundary")
        for seg in range(len(CONFIG.boundary)):
            path_plot = []
            for vertex in range(len(CONFIG.boundary[seg])):
                xplot = int((CONFIG.boundary[seg][vertex][CONFIG.X] * scale + xoff) * CONFIG.window / size)
                path_plot.append(xplot)
                yplot = CONFIG.window - int(
                    (CONFIG.boundary[seg][vertex][CONFIG.Y] * scale + yoff) * CONFIG.window / size)
                path_plot.append(yplot)
                if vert == 1:
                    c.create_text(xplot, yplot, text=str(seg) + ':' + str(vertex), tag="plot_boundary")
            c.create_line(path_plot, tag="plot_boundary")
        GUI.c.delete("plot_path")
        for seg in range(len(CONFIG.toolpath)):
            path_plot = []
            for vertex in range(len(CONFIG.toolpath[seg])):
                xplot = int((CONFIG.toolpath[seg][vertex][CONFIG.X] * scale + xoff) * CONFIG.window / size)
                path_plot.append(xplot)
                yplot = CONFIG.window - int(
                    (CONFIG.toolpath[seg][vertex][CONFIG.Y] * scale + yoff) * CONFIG.window / size)
                path_plot.append(yplot)
                if vert == 1:
                    c.create_text(xplot, yplot, text=str(seg) + ':' + str(vertex), tag="plot_path")
            c.create_line(path_plot, tag="plot_path", fill="red")

    def plot_seg(self, event, CONFIG: Config_Data):
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
                xplot = int((segplot[seg][vertex][CONFIG.X] * scale + xoff) * CONFIG.window / size)
                path_plot.append(xplot)
                yplot = CONFIG.window - int((segplot[seg][vertex][CONFIG.Y] * scale + yoff) * CONFIG.window / size)
                path_plot.append(yplot)
                if vert == 1:
                    c.create_text(xplot, yplot, text=str(seg) + ':' + str(vertex), tag="plot_segment")
            c.create_line(path_plot, tag="plot_segment", fill='white')
            c.create_line(path_plot, tag="plot_segment", fill='blue')

    def plot_delete(self, event, CONFIG: Config_Data, GUI:GUI_Data):
        # global toolpath
        #
        # scale and plot boundary, delete toolpath
        #
        CONFIG.toolpath = []
        print("delete")
        self.plot(event, CONFIG=CONFIG,GUI=GUI)

    def read(self, event, CONFIG: Config_Data):
        inputFileList = CONFIG.inputFileList
        for item in inputFileList:
            if ((item.find(".cmp") != -1) | (item.find(".sol") != -1)
                    | (item.find(".otl") != -1)):
                print(f"Infile Handler: Reading Gerber file: {item}")
                CONFIG.boundary = read_Gerber(item, CONFIG)
            elif item.find(".drl") != -1:
                print(f"Infile Handler: Reading Excellon file: {item}")
                CONFIG.boundary = read_Excellon(item)
                CONFIG.vias = read_ExcellonDrill(item)
            elif item.find(".dxf") != -1:
                print(f"Infile Handler: Reading DXF file: {item}")
                CONFIG.boundary = read_DXF(item)
            else:
                print("unsupported file type")
                return
        CONFIG.toolpath = []
        sum1 = 0
        for segment in range(len(CONFIG.boundary)):
            sum1 += len(CONFIG.boundary[segment])
            for vertex in range(len(CONFIG.boundary[segment])):
                CONFIG.boundary[segment][vertex][CONFIG.X] += gauss(0, CONFIG.noise)
                CONFIG.boundary[segment][vertex][CONFIG.Y] += gauss(0, CONFIG.noise)
                x = CONFIG.boundary[segment][vertex][CONFIG.X]
                y = CONFIG.boundary[segment][vertex][CONFIG.Y]
                if y < CONFIG.ymin:
                    CONFIG.ymin = y
                if y > CONFIG.ymax:
                    CONFIG.ymax = y
                if x < CONFIG.xmin:
                    CONFIG.xmin = x
                if x > CONFIG.xmax:
                    CONFIG.xmax = x
            print(str(segment))
            CONFIG.boundary[segment][-1][CONFIG.X] = CONFIG.boundary[segment][0][CONFIG.X]
            CONFIG.boundary[segment][-1][CONFIG.Y] = CONFIG.boundary[segment][0][CONFIG.Y]
        print("    found", len(CONFIG.boundary), "polygons,", sum1, "vertices")
        print("    added", CONFIG.noise, "perturbation")
        # print(f"    xmin: %0.3g {xmin}xmax: %0.3g {xmax}ymin: %0.3g {ymin}ymax: %0.3g {ymax}")

        self.plot(event)

    def delframes(self, CONFIG: Config_Data, GUI:GUI_Data):
        #
        # delete all CAM frames
        #
        # global cutframe, imgframe, toolframe, millframe, gframe, laserframe
        GUI.cutframe.pack_forget()
        GUI.imgframe.pack_forget()
        GUI.toolframe.pack_forget()
        GUI.millframe.pack_forget()
        GUI.gframe.pack_forget()
        GUI.laserframe.pack_forget()

    def camselect(self, event, CONFIG: Config_Data, GUI: GUI_Data):
        # global size
        #
        # pack appropriate CAM GUI options based on output file
        #
        # global outfile, soverlap, szup, szdown, sxyvel, szvel, sforce, svel, srate, spower, sspeed, sztop, szbottom, sfeed, sspindle, stool, sximg, syimg
        text = CONFIG.outputType()
        if (text.find(".rml") != -1):

            self.delframes(CONFIG=CONFIG,GUI=GUI)
            GUI.sdia = "0.015"
            GUI.sundercut = "0.00"
            GUI.soverlap = "0.8"
            GUI.toolframe.pack()
            GUI.szup = "0.04"
            GUI.szdown = "-0.015"
            GUI.sxyvel = "2"
            GUI.szvel = "5"
            GUI.millframe.pack()
        elif (text.find(".camm") != -1):
            self.delframes(CONFIG=CONFIG,GUI=GUI)
            GUI.sforce = "70"
            GUI.svel = "2"
            GUI.cutframe.pack()
        elif (text.find(".epi") != -1):
            self.delframes(CONFIG=CONFIG,GUI=GUI)
            GUI.srate = "2500"
            GUI.spower = "50"
            GUI.sspeed = "50"
            GUI.ssize = "10"
            GUI.laserframe.pack()
            self.plot(event,CONFIG=CONFIG,GUI=GUI)
        elif (text.find(".g") != -1):
            self.delframes(CONFIG=CONFIG,GUI=GUI)
            GUI.sdia = "0.015"
            GUI.sundercut = "0.00"
            GUI.soverlap = "0.8"
            GUI.toolframe.pack()
            GUI.sztop = "1"
            GUI.szbottom = "0"
            GUI.sfeed = "5"
            GUI.sspindle = "5000"
            GUI.stool = "1"
            GUI.gframe.pack()
        elif ((text.find(".scad") != -1) | text.find(".scad")):
            self.delframes(CONFIG=CONFIG,GUI=GUI)
            GUI.sdia = "0.015"
            GUI.sundercut = "0.01"
            GUI.soverlap = "0.8"
            GUI.toolframe.pack()
            GUI.sztop = "1"
            GUI.szbottom = "0"
            GUI.sfeed = "5"
            GUI.sspindle = "5000"
            GUI.stool = "1"
            GUI.gframe.pack()
        elif ((text.find(".jpg") != -1) | (text.find(".bmp") != -1)):
            self.delframes(CONFIG=CONFIG,GUI=GUI)
            GUI.sdia = "0.015"
            GUI.sundercut = "0.000"
            GUI.soverlap = "0.8"
            GUI.toolframe.pack()
            GUI.sximg = "500"
            GUI.syimg = "500"
            GUI.imgframe.pack()
        else:
            print("output file format not supported")
        return

    def union_boundary(self, event, CONFIG: Config_Data,GUI:GUI_Data):
        # global boundary, intersections
        #
        # union intersecting polygons on boundary
        #
        print("union boundary ...")
        sign = 1
        # boundary = prune(boundary,sign,event)
        CONFIG.boundary = self.new_prune(CONFIG.boundary, sign, event)
        print("    done")
        self.plot(event, CONFIG=CONFIG,GUI=GUI)

    def intersect(self, path, seg0, vert0, sega, verta, CONFIG:Config_Data):
        #
        # test and return edge intersection
        #
        if (seg0 == sega) & (vert0 == 0) & (verta == (len(path[sega]) - 2)):
            # print ("    return (0-end)"
            return [[], []]
        x0 = path[seg0][vert0][CONFIG.X]
        y0 = path[seg0][vert0][CONFIG.Y]
        x1 = path[seg0][vert0 + 1][CONFIG.X]
        y1 = path[seg0][vert0 + 1][CONFIG.Y]
        dx01 = x1 - x0
        dy01 = y1 - y0
        d01 = sqrt(dx01 * dx01 + dy01 * dy01)
        if d01 == 0:
            #
            # zero-length segment, return no intersection
            #
            # print ("zero-length segment"
            return [[], []]
        dxpar01 = dx01 / d01
        dypar01 = dy01 / d01
        dxperp01 = dypar01
        dyperp01 = -dxpar01
        xa = path[sega][verta][CONFIG.X]
        ya = path[sega][verta][CONFIG.Y]
        xb = path[sega][verta + 1][CONFIG.X]
        yb = path[sega][verta + 1][CONFIG.Y]
        dx0a = xa - x0
        dy0a = ya - y0
        dpar0a = dx0a * dxpar01 + dy0a * dypar01
        dperp0a = dx0a * dxperp01 + dy0a * dyperp01
        dx0b = xb - x0
        dy0b = yb - y0
        dpar0b = dx0b * dxpar01 + dy0b * dypar01
        dperp0b = dx0b * dxperp01 + dy0b * dyperp01
        # if (dperp0a*dperp0b > EPS):
        if ((dperp0a > CONFIG.eps) & (dperp0b > CONFIG.eps)) | ((dperp0a < -CONFIG.eps) & (dperp0b < -CONFIG.eps)):
            #
            # vertices on same side, return no intersection
            #
            # print (" same side"
            return [[], []]
        elif (abs(dperp0a) < CONFIG.eps) & (abs(dperp0b) < CONFIG.eps):
            #
            # edges colinear, return no intersection
            #
            # d0a = (xa-x0)*dxpar01 + (ya-y0)*dypar01
            # d0b = (xb-x0)*dxpar01 + (yb-y0)*dypar01
            # print (" colinear"
            return [[], []]
        #
        # calculation distance to intersection
        #
        d = (dpar0a * abs(dperp0b) + dpar0b * abs(dperp0a)) / (abs(dperp0a) + abs(dperp0b))
        if ((d < -CONFIG.eps) | (d > (d01 + CONFIG.eps))):
            #
            # intersection outside segment, return no intersection
            #
            # print ("    found intersection outside segment"
            return [[], []]
        else:
            #
            # intersection in segment, return intersection
            #
            # print ("    found intersection in segment s0 v0 sa va",seg0,vert0,sega,verta
            xloc = x0 + dxpar01 * d
            yloc = y0 + dypar01 * d
            return [xloc, yloc]

    def add_intersections(self, path, GUI:GUI_Data, CONFIG:Config_Data):
        #
        # add vertices at path intersections
        #
        #global status, outframe, namedate
        intersection = 0
        #
        # loop over first edge
        #
        for seg0 in range(len(path)):
            GUI.status.set("    segment " + str(seg0) + "/" + str(len(path) - 1) + "  ")
            GUI.outframe.update()
            vert0 = 0
            N0 = len(path[seg0]) - 1
            while vert0 < N0:
                #
                # loop over second edge
                #
                vert1 = vert0 + 2
                while vert1 < N0:
                    #
                    # check for path self-intersection
                    #
                    [xloc, yloc] = self.intersect(path, seg0, vert0, seg0, vert1)
                    if xloc != []:
                        #
                        # found intersection, insert vertices
                        #
                        n0 = self.insert(path, xloc, yloc, seg0, vert0, intersection)
                        N0 += n0
                        vert1 += n0
                        n1 = self.insert(path, xloc, yloc, seg0, vert1, intersection)
                        N0 += n1
                        vert1 += n1
                        if (n0 > 0) | (n1 > 0):
                            intersection += 1
                    vert1 += 1
                for sega in range((seg0 + 1), len(path)):
                    #
                    # check for intersection with other parts
                    #
                    # outframe.update()
                    verta = 0
                    Na = len(path[sega]) - 1
                    while verta < Na:
                        [xloc, yloc] = self.intersect(path, seg0, vert0, sega, verta)
                        if xloc != []:
                            #
                            # found intersection, insert vertices
                            #
                            n0 = self.insert(path, xloc, yloc, seg0, vert0, intersection)
                            N0 += n0
                            vert1 += n0
                            na = self.insert(path, xloc, yloc, sega, verta, intersection)
                            Na += na
                            verta += na
                            if (n0 > 0) | (na > 0):
                                intersection += 1
                        verta += 1
                vert0 += 1
        #
        # make vertex table and segment list of intersections
        #
        GUI.status.set(CONFIG.namedate)
        GUI.outframe.update()
        intersections = []
        for i in range(intersection):
            intersections.append([])
        for seg in range(len(path)):
            for vert in range(len(path[seg])):
                inters = path[seg][vert][CONFIG.INTERSECT]
                if (inters != []):
                    intersections[inters].append([seg, vert])
        print('    found', len(intersections), 'intersection(s)')
        seg_intersections = []
        for i in range(len(path)):
            seg_intersections.append([])
        for i in range(len(intersections)):
            if (len(intersections[i]) != 2):
                print("    shouldn't happen: i", i, intersections[i])
            else:
                seg_intersections[intersections[i][0][CONFIG.SEG]].append(i)
                seg_intersections[intersections[i][CONFIG.A][CONFIG.SEG]].append(i)
        return [path, intersections, seg_intersections]

    def insert(self, path, x, y, seg, vert, intersection, GUI:GUI_Data, CONFIG:Config_Data):
        #
        # insert a vertex at x,y in seg,vert, if needed
        #
        d0 = (path[seg][vert][CONFIG.X] - x) ** 2 + (path[seg][vert][CONFIG.Y] - y) ** 2
        d1 = (path[seg][vert + 1][CONFIG.X] - x) ** 2 + (path[seg][vert + 1][CONFIG.Y] - y) ** 2
        # print ("check insert seg",seg,"vert",vert,"intersection",intersection
        if ((d0 > CONFIG.eps) & (d1 > CONFIG.eps)):
            # print ("    added intersection vertex",vert+1
            path[seg].insert((vert + 1), [x, y, intersection])
            return 1
        elif (d0 < CONFIG.eps):
            if (path[seg][vert][CONFIG.INTERSECT] == []):
                path[seg][vert][CONFIG.INTERSECT] = intersection
                # print ("    added d0",vert
            return 0
        elif (d1 < CONFIG.eps):
            if (path[seg][vert + 1][CONFIG.INTERSECT] == []):
                path[seg][vert + 1][CONFIG.INTERSECT] = intersection
                # print ("    added d1",vert+1
            return 0
        else:
            # print ("    shouldn't happen: d0",d0,"d1",d1
            return 0

    def new_prune(self, path, sign, event, CONFIG:Config_Data,GUI:GUI_Data):
        #
        # new_prune path intersections
        #
        # first find the intersections
        #
        #global segplot
        print("    intersecting ...")
        # plot_path(event)
        # raw_input('before intersection')
        [path, intersections, seg_intersections] = self.add_intersections(path, CONFIG=CONFIG,GUI=GUI)
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
            if (self.point_in_polygon(point, poly, CONFIG.HUGE)):
                intersections[ii] = []
                print("     Intersection " + str(ii) + "inside poly")
            else:
                point = path[seg1][vert1]
                poly = path[seg0]
                if (self.point_in_polygon(point, poly, CONFIG.HUGE)):
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
            seg = intersections[i][0][CONFIG.SEG]
            vert = intersections[i][0][CONFIG.VERT]
            seg0 = seg
            vert0 = vert
            sega = intersections[i][1][CONFIG.SEG]  # ending segment and vertex
            verta = intersections[i][1][CONFIG.VERT]  # ending segment and vertex
            segplot = []
            segplot.append(path[seg])
            segplot.append(path[sega])
            self.plot_seg(event)
            GUI.status.set("    " + str(i) + ": intersection " + str(i) + "/" + str(len(intersections) - 1) + "  ")
            GUI.outframe.update()
            print("    " + str(i) + ": intersection " + str(i) + "/" + str(len(intersections) - 1) + "  ")
            self.print_intersections(path, intersections, seg)
            intersections[i] = []  # remove this intersection
            vert1 = (vert + 1) % len(path[seg])
            # calculate a point halfway
            point = path[seg][vert]
            point1 = path[seg][vert1]
            point[0] = point[0] + (point1[0] - point[0]) / 2.0
            point[1] = point[1] + (point1[1] - point[1]) / 2.0
            poly = path[sega]
            forward = not self.point_in_polygon(point, poly, CONFIG.HUGE)
            print("     Go forward? " + str(forward))
            newseg = len(newpath)
            newpath.append([])
            x = path[seg][vert][CONFIG.X]
            y = path[seg][vert][CONFIG.Y]
            vertc = 0
            print("      new vertex = " + str(vert))
            newpath[newseg].append([])
            newpath[newseg][vertc] = [x, y, []]
            vertc += 1
            intersectindex = []  # clear next intersection
            while intersectindex != i:  # go all the way around the loop
                if forward:
                    vert = (vert + 1) % len(path[seg])
                else:
                    vert = (vert - 1) % len(path[seg])
                print("      new vertex = " + str(vert))
                intersectindex = path[seg][vert][CONFIG.INTERSECT]
                if intersectindex == []:
                    x = path[seg][vert][CONFIG.X]
                    y = path[seg][vert][CONFIG.Y]
                    newpath[newseg].append([])
                    newpath[newseg][vertc] = [x, y, []]
                    vertc += 1
                elif intersectindex == i:
                    # we've come full circle
                    x = path[seg0][vert0][CONFIG.X]
                    y = path[seg0][vert0][CONFIG.Y]
                    newpath[newseg].append([])
                    newpath[newseg][vertc] = [x, y, []]
                    print("Segment complete [" + str(seg0) + "," + str(vert0) + "] \n\n")
                    break
                else:
                    x = path[seg][vert][CONFIG.X]
                    y = path[seg][vert][CONFIG.Y]
                    newpath[newseg].append([])
                    newpath[newseg][vertc] = [x, y, []]
                    vertc += 1
                    # switch to next segment
                    intersection = intersections[intersectindex]
                    if intersection == []:
                        print("      Intersection erased go on")
                    else:
                        print("     Intersection = " + str(intersectindex))
                        if intersection[0][0] == seg:
                            [seg, vert] = intersection[1]
                            [sega, verta] = intersection[0]
                        else:
                            [seg, vert] = intersection[0]
                            [sega, verta] = intersection[1]
                        print("    New segment [" + str(seg) + "," + str(vert) + "]  Old segment [" + str(
                            sega) + "," + str(verta) + "]\n")
                        segplot.append(path[sega])
                        self.plot_seg(event, CONFIG=CONFIG)
                        GUI.outframe.update()
                        intersections[intersectindex] = []  # remove this intersection
                        self.print_intersections(path, intersections, seg)
                        vert1 = (vert + 1) % len(path[seg])
                        # calculate a point halfway
                        point = path[seg][vert]
                        point1 = path[seg][vert1]
                        point[0] = point[0] + (point1[0] - point[0]) / 2.0
                        point[1] = point[1] + (point1[1] - point[1]) / 2.0
                        poly = path[sega]
                        forward = not self.point_in_polygon(point, poly, CONFIG.HUGE)
                        print("     Go forward? " + str(forward))
                        print("      new vertex = " + str(vert))
                    # end if
                # end if
            # end while
        return newpath

    def print_intersections(self, path, intersections, seg, CONFIG:Config_Data):
        print("    Seg:" + str(seg) + " Intersections found:")
        for ii in range(len(path[seg]) - 1):
            intersect = path[seg][ii][CONFIG.INTERSECT]
            if intersect != []:
                if intersections[intersect] == []:
                    print("     " + str(intersect) + " Erased")
                else:
                    [seg0, vert0] = intersections[intersect][0]
                    [seg1, vert1] = intersections[intersect][1]
                    print(
                        "     " + str(intersect) + " = [" + str(seg0) + "," + str(vert0) + "][" + str(seg1) + "," + str(
                            vert1) + "],")
        return

    def write(self, event, CONFIG: Config_Data):
        # global toolpath, boundary, vias, xmin, xmax, ymin, ymax, gscale
        #
        # write toolpath
        #
        if CONFIG.toolpath == []:
            CONFIG.toolpath = CONFIG.boundary

            # ONLY TESTING FOR GCODE RN
        #texti = self.GUIinfile.get()
        # if (text.find(".rml") != -1):
        #     write_RML(toolpath)
        # elif (text.find(".camm") != -1):
        #     write_CAMM(toolpath)
        # elif (text.find(".epi") != -1):
        #     write_EPI(toolpath)
        if CONFIG.outputType == "GCODE":
            # write_G(toolpath)
            write_G(CONFIG.toolpath, CONFIG)
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
        sxmin = CONFIG.gscale * (CONFIG.xmin + CONFIG.xoff)
        sxmax = CONFIG.gscale * (CONFIG.xmax + CONFIG.xoff)
        symin = CONFIG.gscale * (CONFIG.ymin + CONFIG.yoff)
        symax = CONFIG.gscale * (CONFIG.ymax + CONFIG.yoff)
        print("    xmin: %0.3g " % sxmin, "xmax: %0.3g " % sxmax, "ymin: %0.3g " % symin, "ymax: %0.3g " % symax)

    def point_in_polygon(self, pt, poly, inf):
        result = False
        for i in range(len(poly)-1):
            if self.intersect1(poly[i], poly[i+1], pt, [inf, pt[1]]):
                result = not result
        if self.intersect1(poly[-1], poly[0], pt, (inf, pt[1])):
            result = not result
        return result

    def intersect1(self,A, B, C, D):
        return (self.ccw(A, C, D) != self.ccw(B, C, D)) and (self.ccw(A, B, C) != self.ccw(A, B, D))

    def ccw(self,A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])