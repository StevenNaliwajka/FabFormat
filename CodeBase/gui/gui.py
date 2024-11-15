import tkinter as tk
from CodeBase.config.config import Config

class Gui:
    def __init__(self, CONFIG:Config):

        # CODE BY Neil Gershenfeld.
        # NOT WORKING WITH MY CURRENT DESIGN.
        # HAVE TO RE-WRITE THINGS.
        root = tk.Tk()
        root.title('cam2.py')
        root.bind('q', 'exit')

        infile = tk.StringVar()
        outfile = tk.StringVar()

        inframe = tk.Frame(root)
        tk.Label(inframe, text="input file: ").pack(side="left")
        winfile = tk.Entry(inframe, width=20, textvariable=infile)
        winfile.pack(side="left")
        winfile.bind('<Return>', read)
        ssize = tk.StringVar()
        ssize.set(str(CONFIG.size))
        tk.Label(inframe, text=" ").pack(side="left")
        tk.Label(inframe, text="display size:").pack(side="left")
        wsize = tk.Entry(inframe, width=10, textvariable=ssize)
        wsize.pack(side="left")
        wsize.bind('<Return>', plot)
        tk.Label(inframe, text=" ").pack(side="left")
        ivert = tk.IntVar()
        wvert = tk.Checkbutton(inframe, text="show vertices", variable=ivert)
        wvert.pack(side="left")
        # wvert.bind('<tk.ButtonRelease-1>',plot)
        inframe.pack()

        coordframe = tk.Frame(root)
        sxoff = tk.StringVar()
        sxoff.set(str(xoff))
        syoff = tk.StringVar()
        syoff.set(str(yoff))
        self.sscale = tk.StringVar()
        self.sscale.set(str(scale))
        tk.Label(coordframe, text="x offset:").pack(side="left")
        wxoff = tk.Entry(coordframe, width=10, textvariable=sxoff)
        wxoff.pack(side="left")
        wxoff.bind('<Return>', plot)
        tk.Label(coordframe, text=" y offset:").pack(side="left")
        wyoff = tk.Entry(coordframe, width=10, textvariable=syoff)
        wyoff.pack(side="left")
        wyoff.bind('<Return>', plot)
        tk.Label(coordframe, text=" part scale factor:").pack(side="left")
        wscale = tk.Entry(coordframe, width=10, textvariable=sscale)
        wscale.pack(side="left")
        wscale.bind('<Return>', plot_delete)
        coordframe.pack()

        c = tk.Canvas(root, width=WINDOW, height=WINDOW, background='white')
        c.pack()

        self.outframe = tk.Frame(root)

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
        self.namedate = "    cam.py (" + DATE + ")  "
        status.set(self.namedate)
        tk.Label(outframe, textvariable=status).pack(side="left")
        tk.Label(outframe, text="output file: ").pack(side="left")
        woutfile = tk.Entry(outframe, width=20, textvariable=outfile)
        woutfile.bind('<Return>', camselect)
        woutfile.pack(side="left")
        tk.Label(outframe, text=" ").pack(side="left")
        tk.Button(outframe, text="quit", command='exit').pack(side="left")
        tk.Label(outframe, text=" ").pack(side="left")
        outframe.pack()

        camframe = tk.Frame(root)
        unionbtn = tk.Button(camframe, text="union polygons")
        unionbtn.bind('<Button-1>', union_boundary)
        unionbtn.pack(side="left")
        tk.Label(camframe, text=" ").pack(side="left")
        contourbtn = tk.Button(camframe, text="contour boundary")
        contourbtn.bind('<Button-1>', contour_boundary)
        contourbtn.pack(side="left")
        tk.Label(camframe, text=" ").pack(side="left")
        rasterbtn = tk.Button(camframe, text="raster interior")
        rasterbtn.bind('<Button-1>', raster)
        rasterbtn.pack(side="left")
        tk.Label(camframe, text=" ").pack(side="left")
        writebtn = tk.Button(camframe, text="write toolpath")
        writebtn.bind('<Button-1>', write)
        writebtn.pack(side="left")
        camframe.pack()

        toolframe = tk.Frame(root)
        tk.Label(toolframe, text="tool diameter: ").pack(side="left")
        self.sdia = tk.StringVar()
        wtooldia = tk.Entry(toolframe, width=10, textvariable=sdia)
        wtooldia.pack(side="left")
        wtooldia.bind('<Return>', plot_delete)
        tk.Label(toolframe, text=" contour undercut: ").pack(side="left")
        self.sundercut = tk.StringVar()
        self.wundercut = tk.Entry(toolframe, width=10, textvariable=sundercut)
        wundercut.pack(side="left")
        wundercut.bind('<Return>', plot_delete)
        tk.Label(toolframe, text=" raster overlap: ").pack(side="left")
        soverlap = tk.StringVar()
        woverlap = tk.Entry(toolframe, width=10, textvariable=soverlap)
        woverlap.pack(side="left")
        woverlap.bind('<Return>', plot_delete)

        millframe = tk.Frame(root)
        tk.Label(millframe, text="z up:").pack(side="left")
        szup = tk.StringVar()
        tk.Entry(millframe, width=10, textvariable=szup).pack(side="left")
        tk.Label(millframe, text=" z down:").pack(side="left")
        szdown = tk.StringVar()
        tk.Entry(millframe, width=10, textvariable=szdown).pack(side="left")
        tk.Label(millframe, text=" xy speed:").pack(side="left")
        sxyvel = tk.StringVar()
        tk.Entry(millframe, width=10, textvariable=sxyvel).pack(side="left")
        tk.Label(millframe, text=" z speed:").pack(side="left")
        szvel = tk.StringVar()
        tk.Entry(millframe, width=10, textvariable=szvel).pack(side="left")

        gframe = tk.Frame(root)
        tk.Label(gframe, text="z top:").pack(side="left")
        sztop = tk.StringVar()
        tk.Entry(gframe, width=6, textvariable=sztop).pack(side="left")
        tk.Label(gframe, text=" z bottom:").pack(side="left")
        szbottom = tk.StringVar()
        tk.Entry(gframe, width=6, textvariable=szbottom).pack(side="left")
        tk.Label(gframe, text=" feed rate:").pack(side="left")
        sfeed = tk.StringVar()
        tk.Entry(gframe, width=6, textvariable=sfeed).pack(side="left")
        tk.Label(gframe, text=" spindle speed:").pack(side="left")
        sspindle = tk.StringVar()
        tk.Entry(gframe, width=6, textvariable=sspindle).pack(side="left")
        tk.Label(gframe, text=" tool:").pack(side="left")
        stool = tk.StringVar()
        tk.Entry(gframe, width=3, textvariable=stool).pack(side="left")

        cutframe = tk.Frame(root)
        tk.Label(cutframe, text="force: ").pack(side="left")
        sforce = tk.StringVar()
        tk.Entry(cutframe, width=10, textvariable=sforce).pack(side="left")
        tk.Label(cutframe, text=" velocity:").pack(side="left")
        svel = tk.StringVar()
        tk.Entry(cutframe, width=10, textvariable=svel).pack(side="left")

        laserframe = tk.Frame(root)
        tk.Label(laserframe, text="rate: ").pack(side="left")
        srate = tk.StringVar()
        tk.Entry(laserframe, width=10, textvariable=srate).pack(side="left")
        tk.Label(laserframe, text=" power:").pack(side="left")
        spower = tk.StringVar()
        tk.Entry(laserframe, width=10, textvariable=spower).pack(side="left")
        tk.Label(laserframe, text=" speed:").pack(side="left")
        sspeed = tk.StringVar()
        tk.Entry(laserframe, width=10, textvariable=sspeed).pack(side="left")

        imgframe = tk.Frame(root)
        tk.Label(imgframe, text="x size (pixels): ").pack(side="left")
        sximg = tk.StringVar()
        tk.Entry(imgframe, width=10, textvariable=sximg).pack(side="left")
        tk.Label(imgframe, text=" y size (pixels):").pack(side="left")
        syimg = tk.StringVar()
        tk.Entry(imgframe, width=10, textvariable=syimg).pack(side="left")

        camselect(0)

        if (len(infile.get()) != 0):
            read(0)

        root.mainloop()