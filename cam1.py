#
# cam.py
#
# usage: python cam.py [infile] [xoffset yoffset] [display size] [outfile] [undercut]
#
# input:
#     *.dxf: DXF (polylines)
#     *.cmp,*.sol,*.plc: Gerber
#         RS-274X format, with 0-width trace defining board boundary
#     *.drl: Excellon drill file, with tool defitions
# output:
#     *.rml: Roland Modela RML mill
#     *.camm: Roland CAMM cutter
#     *.jpg,*.bmp: images
#     *.epi: Epilog lasercutter
#     *.g: G codes
# toolpath modes: 1D path, contour, raster
# keys: q to quit
#
# (C)BA Neil Gershenfeld
# commercial sale licensed by MIT
DATE = "11/9/03"

#from Tkinter import *
from string import *
from math import *
from random import *
#from Pillow import *
import sys  
# import Image
# import ImageDraw 
import tkinter as tk

#
# window size in pixels
#
WINDOW = 500
#
# numerical roundoff tolerance for testing intersections
#
EPS = 1e-20
#
# hack: std dev of numerical noise to add to remove degeneracies
#
NOISE = 1e-6
#
# default parameters
#
scale = 1.0
gscale = 25.4 # assuming gerber is in inches and scad must be in mm

sthickness = 0.1 # substrate thickness
mthickness = 0.0075 # metal thickness in inches 0.19mm
mwidth = 0.01 # conductor width in inces 0.25mm
size = 2.0
xoff = 0.1
yoff = 0.1

boundary = []
toolpath = []
itoolpath = [] 
infile = []
segplot = []
vias = []

HUGE = 1e10
xmin = HUGE
xmax = -HUGE
ymin = HUGE
ymax = -HUGE

X = 0
Y = 1
INTERSECT = 2

SEG = 0
VERT = 1
A = 1

TYPE = 0
SIZE = 1
WIDTH = 1
HEIGHT = 2
NVERTS = 10
TRUE = 1
FALSE = 0

def coord(tstr,digits,fraction):
    #
    # parse Gerber coordinates
    #
    global gerbx, gerby
    xindex = tstr.find("X")
    yindex = tstr.find("Y")
    index = tstr.find("D")
    if (xindex == -1):
        x = gerbx
        y = int(tstr[(yindex+1):index])*(10**(-fraction))
    elif (yindex == -1):
        y = gerby
        x = int(tstr[(xindex+1):index])*(10**(-fraction))
    else:
        x = int(tstr[(xindex+1):yindex])*(10**(-fraction))
        y = int(tstr[(yindex+1):index])*(10**(-fraction))
    gerbx = x
    gerby = y
    return [x,y]

def read_Gerber(tstr):
    #
    # Gerber parser
    #
    print(tstr)
    segment = -1
    xold = []
    yold = []
    line = 0
    nlines = len(tstr)
    print(f"HERE: {nlines}")
    path = []
    apertures = []
    macros = []
    N_macros = 0
    for i in range(1000):
        apertures.append([])
    while line < nlines:
        if (tstr[line].find("%FS") != -1):
            #
            # format statement
            #
            index = tstr[line].find("X")
            digits = int(tstr[line][index+1])
            fraction = int(tstr[line][index+2])
            line += 1
            continue
        elif (tstr[line].find("%AM") != -1):
            #
            # aperture macro
            #
            index = tstr[line].find("%AM")
            index1 = tstr[line].find("*")
            macros.append([])
            macros[-1] = tstr[line][index+3:index1]
            N_macros += 1
            line += 1
            continue
        elif (tstr[line].find("%ADD") != -1):
            #
            # aperture definition
            #
            index = tstr[line].find("%ADD")
            parse = 0
            if (tstr[line].find("C,") != -1):
                #
                # circle
                #
                index = tstr[line].find("C,")
                index1 = tstr[line].find("*")
                aperture = int(tstr[line][4:index])
                size = float(tstr[line][index+2:index1])
                apertures[aperture] = ["C",size]
                print ("    read aperture",aperture,": circle diameter",size)
                line += 1
                continue
            elif (tstr[line].find("O,") != -1):
                #
                # obround
                #
                index = tstr[line].find("O,")
                aperture = int(tstr[line][4:index])
                index1 = tstr[line].find(",",index)
                index2 = tstr[line].find("X",index)
                index3 = tstr[line].find("*",index)
                width = float(tstr[line][index1+1:index2])
                height = float(tstr[line][index2+1:index3])
                apertures[aperture] = ["O",width,height]
                print ("    read aperture",aperture,": obround",width,"x",height)
                line += 1
                continue
            elif (tstr[line].find("R,") != -1):
                #
                # rectangle
                #
                index = tstr[line].find("R,")
                aperture = int(tstr[line][4:index])
                index1 = tstr[line].find(",",index)
                index2 = tstr[line].find("X",index)
                index3 = tstr[line].find("*",index)
                width = float(tstr[line][index1+1:index2])
                height = float(tstr[line][index2+1:index3])
                apertures[aperture] = ["R",width,height]
                print ("    read aperture",aperture,": rectangle",width,"x",height)
                line += 1
                continue
            for macro in range(N_macros):
                #
                # macros
                #
                index = tstr[line].find(macros[macro]+',')
                if (index != -1):
                    #
                    # hack: assume macros can be approximated by
                    # a circle, and has a size parameter
                    #
                    aperture = int(tstr[line][4:index])
                    index1 = tstr[line].find(",",index)
                    index2 = tstr[line].find("*",index)
                    size = float(tstr[line][index1+1:index2])
                    apertures[aperture] = ["C",size]
                    print ("    read aperture",aperture,": macro (assuming circle) diameter",size)
                    parse = 1
                    continue
            if (parse == 0):
                print ("    aperture not implemented:",tstr[line])
                return
        elif (tstr[line].find("D") == 0):
            #
            # change aperture
            #
            index = tstr[line].find('*')
            aperture = int(tstr[line][1:index])
            size = apertures[aperture][SIZE]
            line += 1
            continue
        elif (tstr[line].find("G54D") == 0):
            #
            # change aperture
            #
            index = tstr[line].find('*')
            aperture = int(tstr[line][4:index])
            size = apertures[aperture][SIZE]
            line += 1
            continue
        elif (tstr[line].find("D01*") != -1):
            #
            # pen down
            #
            [xnew,ynew] = coord(tstr[line],digits,fraction)
            line += 1
            if (size > EPS):
                if ((abs(xnew-xold) > EPS) | (abs(ynew-yold) > EPS)):
                    newpath = stroke(xold,yold,xnew,ynew,size)
                    path.append(newpath)
                    segment += 1
            else:
                path[segment].append([xnew,ynew,[]])
            xold = xnew
            yold = ynew
            continue
        elif (tstr[line].find("D02*") != -1):
            #
            # pen up
            #
            [xold,yold] = coord(tstr[line],digits,fraction)
            if (size < EPS):
                path.append([])
                segment += 1
                path[segment].append([xold,yold,[]])
            newpath = []
            line += 1
            continue
        elif (tstr[line].find("D03*") != -1):
            #
            # flash
            #
            [xnew,ynew] = coord(tstr[line],digits,fraction)
            line += 1
            if (apertures[aperture][TYPE] == "C"):
                #
                # circle
                #
                path.append([])
                segment += 1    
                size = apertures[aperture][SIZE]
                for i in range(NVERTS):
                    angle = i*2.0*pi/(NVERTS-1.0)
                    x = xnew + (size/2.0)*cos(angle)
                    y = ynew + (size/2.0)*sin(angle)
                    path[segment].append([x,y,[]])
            elif (apertures[aperture][TYPE] == "R"):
                #
                # rectangle
                #
                path.append([])
                segment += 1    
                width = apertures[aperture][WIDTH] / 2.0
                height = apertures[aperture][HEIGHT] / 2.0
                path[segment].append([xnew-width,ynew-height,[]])
                path[segment].append([xnew+width,ynew-height,[]])
                path[segment].append([xnew+width,ynew+height,[]])
                path[segment].append([xnew-width,ynew+height,[]])
                path[segment].append([xnew-width,ynew-height,[]])
            elif (apertures[aperture][TYPE] == "O"):
                #
                # obround
                #
                path.append([])
                segment += 1    
                width = apertures[aperture][WIDTH]
                height = apertures[aperture][HEIGHT]
                if (width > height):
                    for i in range(NVERTS/2):
                        angle = i*pi/(NVERTS/2-1.0) + pi/2.0
                        x = xnew - (width-height)/2.0 + (height/2.0)*cos(angle)
                        y = ynew + (height/2.0)*sin(angle)
                        path[segment].append([x,y,[]])
                    for i in range(NVERTS/2):
                        angle = i*pi/(NVERTS/2-1.0) - pi/2.0
                        x = xnew + (width-height)/2.0 + (height/2.0)*cos(angle)
                        y = ynew + (height/2.0)*sin(angle)
                        path[segment].append([x,y,[]])
                else:
                    for i in range(NVERTS/2):
                        angle = i*pi/(NVERTS/2-1.0) + pi
                        x = xnew + (width/2.0)*cos(angle)
                        y = ynew - (height-width)/2.0 + (width/2.0)*sin(angle)
                        path[segment].append([x,y,[]])
                    for i in range(NVERTS/2):
                        angle = i*pi/(NVERTS/2-1.0)
                        x = xnew + (width/2.0)*cos(angle)
                        y = ynew + (height-width)/2.0 + (width/2.0)*sin(angle)
                        path[segment].append([x,y,[]])
                x = path[segment][-1][X]
                y = path[segment][-1][Y]
                path[segment].append([x,y,[]])
            else:
                print ("    aperture",apertures[aperture][TYPE],"is not implemented")
                return
            xold = xnew
            yold = ynew
            continue
        else:
            print ("    not parsed:",tstr[line])
        line += 1
    return path

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

def read(event):
    global boundary, vias, toolpath, xmin, xmax, ymin, ymax
    #
    # read file
    #
    text = infile.get()
    file = open(text, 'r')
    tstr = file.readlines()
    for item in tstr:
        if ((item.find(".cmp") != -1) | (item.find(".sol")!= -1) \
            | (item.find(".otl")!= -1)):
            print ("reading Gerber file",item)
            boundary = read_Gerber(item)
        elif (item.find(".drl") != -1):
            print ("reading Excellon file",item)
            boundary = read_Excellon(tstr)
            vias = read_ExcellonDrill(tstr)
        elif (item.find(".dxf") != -1):
            print ("reading DXF file",text)
            boundary = read_DXF(tstr)
        else:
            print ("unsupported file type")
            return
        file.close()
    toolpath = []
    sum1 = 0
    for segment in range(len(boundary)):
        sum1 += len(boundary[segment])
        for vertex in range(len(boundary[segment])):
            boundary[segment][vertex][X] += gauss(0,NOISE)
            boundary[segment][vertex][Y] += gauss(0,NOISE)
            x = boundary[segment][vertex][X]
            y = boundary[segment][vertex][Y]
            if (y < ymin): ymin = y
            if (y > ymax): ymax = y
            if (x < xmin): xmin = x
            if (x > xmax): xmax = x
        print(str(segment))
        boundary[segment][-1][X] = boundary[segment][0][X]
        boundary[segment][-1][Y] = boundary[segment][0][Y]
    print ("    found",len(boundary),"polygons,",sum1,"vertices")
    print ("    added",NOISE,"perturbation")
    print ("    xmin: %0.3g "%xmin,"xmax: %0.3g "%xmax,"ymin: %0.3g "%ymin,"ymax: %0.3g "%ymax)
    plot(event)

def stroke(x0,y0,x1,y1,width):
    #
    # stroke segment with width
    #
    #print ("stroke:",x0,y0,x1,y1,width
    global NVERTS
    itemp = 0
    dx = x1 - x0
    dy = y1 - y0
    d = sqrt(dx*dx + dy*dy)
    dxpar = dx / d
    dypar = dy / d
    dxperp = dypar
    dyperp = -dxpar
    dx = -dxperp * width/2.0
    dy = -dyperp * width/2.0
    angle = pi/(NVERTS/2-1.0)
    c = cos(angle)
    s = sin(angle)
    newpath = []
    for i in range(int(NVERTS/2)):#NVERTS/2):
        newpath.append([x0+dx,y0+dy,[]])
        [dx,dy] = [c*dx-s*dy, s*dx+c*dy]
    dx = dxperp * width/2.0
    dy = dyperp * width/2.0
    for i in range(int(NVERTS/2)):
        newpath.append([x1+dx,y1+dy,[]])
        [dx,dy] = [c*dx-s*dy, s*dx+c*dy]
    itemp = itemp + 2*i # This is only here to turn off the warning that i is not used
    x0 = newpath[0][X]
    y0 = newpath[0][Y]
    newpath.append([x0,y0,[]])
    return newpath

def plot(event):
    global boundary, toolpath, ssize, sscale, sxoff, syoff, ivert, c
    #
    # scale and plot boundary and toolpath
    #
    size = float(ssize.get())
    scale = float(sscale.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    vert = ivert.get()
    c.delete("plot_boundary")
    for seg in range(len(boundary)):
        path_plot = []
        for vertex in range (len(boundary[seg])):
            xplot = int((boundary[seg][vertex][X]*scale + xoff)*WINDOW/size)
            path_plot.append(xplot)
            yplot = WINDOW - int((boundary[seg][vertex][Y]*scale + yoff)*WINDOW/size)
            path_plot.append(yplot)
            if (vert == 1):
                c.create_text(xplot,yplot,text=str(seg)+':'+str(vertex),tag="plot_boundary")
        c.create_line(path_plot,tag="plot_boundary")
    c.delete("plot_path")
    for seg in range(len(toolpath)):
        path_plot = []
        for vertex in range (len(toolpath[seg])):
            xplot = int((toolpath[seg][vertex][X]*scale + xoff)*WINDOW/size)
            path_plot.append(xplot)
            yplot = WINDOW - int((toolpath[seg][vertex][Y]*scale + yoff)*WINDOW/size)
            path_plot.append(yplot)
            if (vert == 1):
                c.create_text(xplot,yplot,text=str(seg)+':'+str(vertex),tag="plot_path")
        c.create_line(path_plot,tag="plot_path",fill="red")

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
        for vertex in range (len(segplot[seg])):
            xplot = int((segplot[seg][vertex][X]*scale + xoff)*WINDOW/size)
            path_plot.append(xplot)
            yplot = WINDOW - int((segplot[seg][vertex][Y]*scale + yoff)*WINDOW/size)
            path_plot.append(yplot)
            if (vert == 1):
                c.create_text(xplot,yplot,text=str(seg)+':'+str(vertex),tag="plot_segment")
        c.create_line(path_plot,tag="plot_segment",fill='white')
        c.create_line(path_plot,tag="plot_segment",fill='blue')

def plot_delete(event):
    global toolpath
    #
    # scale and plot boundary, delete toolpath
    #
    toolpath = []
    print ("delete")
    plot(event)

def intersect(path,seg0,vert0,sega,verta):
    #
    # test and return edge intersection
    #
    if ((seg0 == sega) & (vert0 == 0) & (verta == (len(path[sega])-2))):
        #print ("    return (0-end)"
        return [[],[]]
    x0 = path[seg0][vert0][X]
    y0 = path[seg0][vert0][Y]
    x1 = path[seg0][vert0+1][X]
    y1 = path[seg0][vert0+1][Y]
    dx01 = x1 - x0
    dy01 = y1 - y0
    d01 = sqrt(dx01*dx01 + dy01*dy01)
    if (d01 == 0):
        #
        # zero-length segment, return no intersection
        #
        #print ("zero-length segment"
        return [[],[]]
    dxpar01 = dx01 / d01
    dypar01 = dy01 / d01
    dxperp01 = dypar01
    dyperp01 = -dxpar01
    xa = path[sega][verta][X]
    ya = path[sega][verta][Y]
    xb = path[sega][verta+1][X]
    yb = path[sega][verta+1][Y]
    dx0a = xa - x0
    dy0a = ya - y0
    dpar0a = dx0a*dxpar01 + dy0a*dypar01
    dperp0a = dx0a*dxperp01 + dy0a*dyperp01
    dx0b = xb - x0
    dy0b = yb - y0
    dpar0b = dx0b*dxpar01 + dy0b*dypar01
    dperp0b = dx0b*dxperp01 + dy0b*dyperp01
    #if (dperp0a*dperp0b > EPS):
    if (((dperp0a > EPS) & (dperp0b > EPS)) | ((dperp0a < -EPS) & (dperp0b < -EPS))):
        #
        # vertices on same side, return no intersection
        #
        #print (" same side"
        return [[],[]]
    elif ((abs(dperp0a) < EPS) & (abs(dperp0b) < EPS)):
        #
        # edges colinear, return no intersection
        #
        #d0a = (xa-x0)*dxpar01 + (ya-y0)*dypar01
        #d0b = (xb-x0)*dxpar01 + (yb-y0)*dypar01
        #print (" colinear"
        return [[],[]]
    #
    # calculation distance to intersection
    #
    d = (dpar0a*abs(dperp0b)+dpar0b*abs(dperp0a))/(abs(dperp0a)+abs(dperp0b))
    if ((d < -EPS) | (d > (d01+EPS))):
        #
        # intersection outside segment, return no intersection
        #
        #print ("    found intersection outside segment"
        return [[],[]]
    else:
        #
        # intersection in segment, return intersection
        #
        #print ("    found intersection in segment s0 v0 sa va",seg0,vert0,sega,verta
        xloc = x0 + dxpar01*d
        yloc = y0 + dypar01*d
        return [xloc,yloc]

def union(i,path,intersections,sign):
    #
    # return edge to exit intersection i for a union
    #
    #print ("union: intersection",i,"in",intersections
    seg0 = intersections[i][0][SEG]
    #print ("seg0",seg0
    vert0 = intersections[i][0][VERT]
    x0 = path[seg0][vert0][X]
    y0 = path[seg0][vert0][Y]
    if (vert0 < (len(path[seg0])-1)):
        vert1 = vert0 + 1
    else:
        vert1 = 0
    x1 = path[seg0][vert1][X]
    y1 = path[seg0][vert1][Y]
    dx01 = x1-x0
    dy01 = y1-y0
    sega = intersections[i][A][SEG]
    verta = intersections[i][A][VERT]
    xa = path[sega][verta][X]
    ya = path[sega][verta][Y]
    if (verta < (len(path[sega])-1)):
        vertb = verta + 1
    else:
        vertb = 0
    xb = path[sega][vertb][X]
    yb = path[sega][vertb][Y]
    dxab = xb-xa
    dyab = yb-ya
    dot = dxab*dy01 - dyab*dx01
    #print ("    dot",dot)
    if (abs(dot) <= EPS):
        print ("  colinear")
        seg = []
        vert= []
    elif (dot > EPS):
        seg = intersections[i][int((1-sign)/2)][SEG]
        vert = intersections[i][int((1-sign)/2)][VERT]
    else:
        seg = intersections[i][int((1+sign)/2)][SEG]
        vert = intersections[i][int((1+sign)/2)][VERT]
    return [seg,vert]

def insert(path,x,y,seg,vert,intersection):
    #
    # insert a vertex at x,y in seg,vert, if needed
    #
    d0 = (path[seg][vert][X]-x)**2 + (path[seg][vert][Y]-y)**2
    d1 = (path[seg][vert+1][X]-x)**2 + (path[seg][vert+1][Y]-y)**2
    #print ("check insert seg",seg,"vert",vert,"intersection",intersection
    if ((d0 > EPS) & (d1 > EPS)):
        #print ("    added intersection vertex",vert+1
        path[seg].insert((vert+1),[x,y,intersection])
        return 1
    elif (d0 < EPS):
        if (path[seg][vert][INTERSECT] == []):
            path[seg][vert][INTERSECT] = intersection
            #print ("    added d0",vert
        return 0
    elif (d1 < EPS):
        if (path[seg][vert+1][INTERSECT] == []):
            path[seg][vert+1][INTERSECT] = intersection
            #print ("    added d1",vert+1
        return 0
    else:
        #print ("    shouldn't happen: d0",d0,"d1",d1
        return 0

def add_intersections(path):
    #
    # add vertices at path intersections
    #
    global status, outframe, namedate
    intersection = 0
    #
    # loop over first edge
    #
    for seg0 in range(len(path)):
        status.set("    segment "+str(seg0)+"/"+str(len(path)-1)+"  ")
        outframe.update()
        vert0 = 0
        N0 = len(path[seg0])-1
        while (vert0 < N0):
            #
            # loop over second edge
            #
            vert1 = vert0 + 2
            while (vert1 < N0):
                #
                # check for path self-intersection
                #
                [xloc,yloc] = intersect(path,seg0,vert0,seg0,vert1)
                if (xloc != []):
                    #
                    # found intersection, insert vertices
                    #
                    n0 = insert(path,xloc,yloc,seg0,vert0,intersection)
                    N0 += n0
                    vert1 += n0
                    n1 = insert(path,xloc,yloc,seg0,vert1,intersection)
                    N0 += n1
                    vert1 += n1
                    if ((n0 > 0) | (n1 > 0)):
                        intersection += 1
                vert1 += 1
            for sega in range((seg0+1),len(path)):
                #
                # check for intersection with other parts
                #
                #outframe.update()
                verta = 0
                Na = len(path[sega])-1
                while (verta < Na):
                    [xloc,yloc] = intersect(path,seg0,vert0,sega,verta)
                    if (xloc != []):
                        #
                        # found intersection, insert vertices
                        #
                        n0 = insert(path,xloc,yloc,seg0,vert0,intersection)
                        N0 += n0
                        vert1 += n0
                        na = insert(path,xloc,yloc,sega,verta,intersection)
                        Na += na
                        verta += na
                        if ((n0 > 0) | (na > 0)):
                            intersection += 1
                    verta += 1
            vert0 += 1
    #
    # make vertex table and segment list of intersections
    #
    status.set(namedate)
    outframe.update()
    intersections = []
    for i in range(intersection):
        intersections.append([]) 
    for seg in range(len(path)):
        for vert in range(len(path[seg])):
            inters = path[seg][vert][INTERSECT]
            if (inters != []):
                intersections[inters].append([seg,vert])
    print ('    found',len(intersections),'intersection(s)')
    seg_intersections = []
    for i in range(len(path)): 
        seg_intersections.append([])
    for i in range(len(intersections)):
        if (len(intersections[i]) != 2):
            print ("    shouldn't happen: i",i,intersections[i])
        else:
            seg_intersections[intersections[i][0][SEG]].append(i)
            seg_intersections[intersections[i][A][SEG]].append(i)
    return [path, intersections, seg_intersections]

def offset(x0,x1,x2,y0,y1,y2,r):
    #
    # calculate offset by r for vertex 1
    #
    dx0 = x1 - x0
    dx1 = x2 - x1
    dy0 = y1 - y0
    dy1 = y2 - y1
    d0 = sqrt(dx0*dx0 + dy0*dy0)
    d1 = sqrt(dx1*dx1 + dy1*dy1)
    if ((d0 == 0) | (d1 == 0)):
        return [[],[]]
    dx0par = dx0 / d0
    dy0par = dy0 / d0
    dx0perp = dy0 / d0
    dy0perp = -dx0 / d0
    dx1perp = dy1 / d1
    dy1perp = -dx1 / d1
    #print ("offset points:",x0,x1,x2,y0,y1,y2
    #print ("offset normals:",dx0perp,dx1perp,dy0perp,dy1perp
    if ((abs(dx0perp*dy1perp - dx1perp*dy0perp) < EPS) | \
          (abs(dy0perp*dx1perp - dy1perp*dx0perp) < EPS)):
        dx = r * dx1perp
        dy = r * dy1perp
        #print ("    offset planar:",dx,dy
    elif ((abs(dx0perp+dx1perp) < EPS) & (abs(dy0perp+dy1perp) < EPS)):
        dx = r * dx0par
        dy = r * dy0par
        #print ("    offset hairpin:",dx,dy
    else:
        dx = r*(dy1perp - dy0perp) / \
              (dx0perp*dy1perp - dx1perp*dy0perp)
        dy = r*(dx1perp - dx0perp) / \
              (dy0perp*dx1perp - dy1perp*dx0perp)
        #print ("    offset OK:",dx,dy
    return [dx,dy]

def displace(path):
    #
    # displace path inwards by tool radius if negitive
    #
    global sundercut, sdia
    newpath = []
    scale = float(sscale.get())
    undercut = float(sundercut.get())
    toolrad =(float(sdia.get())/2.0-undercut)/scale
    for seg in range(len(path)):
        newpath.append([])
        if (len(path[seg]) > 2):
            for vert1 in range(len(path[seg])-1):
                if (vert1 == 0):
                    vert0 = len(path[seg]) - 2
                else:
                    vert0 = vert1 - 1
                vert2 = vert1 + 1
                x0 = path[seg][vert0][X]
                x1 = path[seg][vert1][X]
                x2 = path[seg][vert2][X]
                y0 = path[seg][vert0][Y]
                y1 = path[seg][vert1][Y]
                y2 = path[seg][vert2][Y]
                [dx,dy] = offset(x0,x1,x2,y0,y1,y2,toolrad)
                if (dx != []):
                    newpath[seg].append([(x1+dx),(y1+dy),[]])
                    if (vert1 == 0):
                        xo = x1+dx
                        yo = y1+dy
                    x0 = newpath[seg][0][X]
                    y0 = newpath[seg][0][Y]
                elif (len(path[seg]) == 2):
                    x0 = path[seg][0][X]
                    y0 = path[seg][0][Y]
                    x1 = path[seg][1][X]
                    y1 = path[seg][1][Y]
                    x2 = 2*x1 - x0
                    y2 = 2*y1 - y0
                    [dx,dy] = offset(x0,x1,x2,y0,y1,y2,toolrad)
            newpath[seg].append([xo,yo,[]])
            x0 = newpath[seg][0][X]
            y0 = newpath[seg][0][Y]
            newpath[seg].append([x0,y0,[]])
        else:
            print ("  displace: shouldn't happen")
    return newpath



def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect1(A,B,C,D):
    return (ccw(A,C,D) != ccw(B,C,D)) and (ccw(A,B,C) != ccw(A,B,D))

def point_in_polygon(pt, poly, inf):
    result = False
    for i in range(len(poly)-1):
        if intersect1(poly[i], poly[i+1], pt, [inf, pt[1]]):
            result = not result
    if intersect1(poly[-1], poly[0], pt, (inf, pt[1])):
        result = not result
    return result

def in_me(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if ((p1x == p2x) or (x <= xints)):
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def print_intersections(path,intersections,seg):
    print("    Seg:"+str(seg)+" Intersections found:")
    for ii in range(len(path[seg])-1):
        intersect = path[seg][ii][INTERSECT]
        if (intersect != []):
            if (intersections[intersect] == []):
                print("     "+str(intersect)+" Erased")
            else:
                [seg0,vert0] = intersections[intersect][0]
                [seg1,vert1] = intersections[intersect][1]
                print("     "+str(intersect)+" = ["+str(seg0)+","+str(vert0)+"]["+str(seg1)+","+str(vert1)+"],")
    return

def new_prune(path,sign,event):
    #
    # new_prune path intersections
    #
    # first find the intersections
    #
    global segplot
    print ("    intersecting ...")
    #plot_path(event)
    #raw_input('before intersection')
    [path, intersections, seg_intersections] = add_intersections(path)
    #print ('path:',path)
    #print ('intersections:',intersections)
    #print ('seg_intersections:',seg_intersections)
    #plot_boundary(event)
    #plot_path(event)
    #raw_input('after intersection')
    print ("intersected")
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
    for ii in range(len(intersections)-1):
        [seg0,vert0] = intersections[ii][0]
        [seg1,vert1] = intersections[ii][1]
        point = path[seg0][vert0]
        poly = path[seg1]
        if (point_in_polygon(point,poly,HUGE)):
            intersections[ii] = []
            print("     Intersection "+str(ii)+"inside poly")
        else:                 
            point = path[seg1][vert1]
            poly = path[seg0]
            if (point_in_polygon(point,poly,HUGE)):
                intersections[ii] = []
                print("     Intersection "+str(ii)+"inside poly")
            # end if
        #end else
    #end for   
    #
    # finally follow each outer path and remove the intersections as we go
    #
    print ("    pruning ...")
    i = 0
    newseg = 0
    for i in range(len(intersections)):
        if (intersections[i] == []):
            #
            # skip null intersections
            #
            i += 1
            continue
        #else:
        #   istart = i
        #   get the segment in the first intersection
        seg = intersections[i][0][SEG]
        vert = intersections[i][0][VERT]
        seg0 = seg
        vert0 = vert
        sega = intersections[i][1][SEG] #ending segment and vertex
        verta = intersections[i][1][VERT] #ending segment and vertex
        segplot = []
        segplot.append(path[seg])
        segplot.append(path[sega]) 
        plot_seg(event)
        status.set("    "+str(i)+": intersection "+str(i)+"/"+str(len(intersections)-1)+"  ")
        outframe.update()
        print("    "+str(i)+": intersection "+str(i)+"/"+str(len(intersections)-1)+"  ")
        print_intersections(path,intersections,seg)
        intersections[i] = [] # remove this intersection
        vert1 = (vert+1)%len(path[seg])
        # calculate a point halfway
        point = path[seg][vert]
        point1 = path[seg][vert1]
        point[0] = point[0]+(point1[0]-point[0])/2.0
        point[1] = point[1]+(point1[1]-point[1])/2.0
        poly = path[sega] 
        forward = not point_in_polygon(point,poly,HUGE)
        print ("     Go forward? " + str(forward))
        newseg = len(newpath)
        newpath.append([])
        x = path[seg][vert][X]
        y = path[seg][vert][Y]
        vertc = 0
        print ("      new vertex = "+str(vert))
        newpath[newseg].append([])
        newpath[newseg][vertc] = [x,y,[]]
        vertc += 1
        intersectindex = [] # clear next intersection
        while ( intersectindex != i ):  # go all the way around the loop
            if (forward):
                vert = (vert + 1)%len(path[seg])
            else:
                vert = (vert - 1)%len(path[seg])
            print ("      new vertex = "+str(vert))
            intersectindex = path[seg][vert][INTERSECT]
            if (intersectindex == []):
                x = path[seg][vert][X]
                y = path[seg][vert][Y]
                newpath[newseg].append([])
                newpath[newseg][vertc] = [x,y,[]]
                vertc += 1
            elif (intersectindex == i):
                # we've come full circle
                x = path[seg0][vert0][X]
                y = path[seg0][vert0][Y]
                newpath[newseg].append([])
                newpath[newseg][vertc] = [x,y,[]]
                print (     "Segment complete ["+str(seg0)+","+str(vert0)+"] \n\n")
                break
            else:
                x = path[seg][vert][X]
                y = path[seg][vert][Y]
                newpath[newseg].append([])
                newpath[newseg][vertc] = [x,y,[]]
                vertc += 1
                # switch to next segment
                intersection = intersections[intersectindex]
                if (intersection == []):
                    print("      Intersection erased go on")
                else:
                    print ("     Intersection = "+str(intersectindex))
                    if (intersection[0][0] == seg):
                        [seg, vert] = intersection[1]
                        [sega,verta] = intersection[0]
                    else:
                        [seg,vert] = intersection[0]
                        [sega,verta] = intersection[1]
                    print("    New segment ["+str(seg)+","+str(vert)+"]  Old segment ["+str(sega)+","+str(verta)+"]\n")
                    segplot.append(path[sega]) 
                    plot_seg(event)
                    outframe.update()
                    intersections[intersectindex] = [] # remove this intersection
                    print_intersections(path,intersections,seg)
                    vert1 = (vert+1)%len(path[seg])
                    # calculate a point halfway
                    point = path[seg][vert]
                    point1 = path[seg][vert1]
                    point[0] = point[0]+(point1[0]-point[0])/2.0
                    point[1] = point[1]+(point1[1]-point[1])/2.0
                    poly = path[sega] 
                    forward = not point_in_polygon(point,poly,HUGE)
                    print ("     Go forward? " + str(forward))
                    print ("      new vertex = "+str(vert))
                #end if
            # end if        
        #end while
    return newpath

def prune(path,sign,event):
    #
    # prune path intersections
    #
    # first find the intersections
    #
    print ("    intersecting ...")
    #plot_path(event)
    #raw_input('before intersection')
    [path, intersections, seg_intersections] = add_intersections(path)
    #print 'path:',path
    #print 'intersections:',intersections
    #print 'seg_intersections:',seg_intersections
    #plot_boundary(event)
    #plot_path(event)
    #raw_input('after intersection')
    print ("intersected")
    #
    # then copy non-intersecting segments to new path
    #
    newpath = []
    for seg in range(len(seg_intersections)):
        if (seg_intersections[seg] == []):
            newpath.append(path[seg])
    #
    # finally follow and remove the intersections
    #
    print ("    pruning ...")
    i = 0
    newseg = 0
    while (i < len(intersections)):
        if (intersections[i] == []):
            #
            # skip null intersections
            #
            i += 1
        else:
            istart = i
            intersection = istart
            #
            # skip interior intersections
            #
            oldseg = -1
            interior = TRUE
            while 1:
                #print 'testing intersection',intersection,':',intersections[intersection]
                if (intersections[intersection] == []):
                    seg = oldseg
                else:
                    [seg,vert] = union(intersection,path,intersections,sign)
                    #print '  seg',seg,'vert',vert,'oldseg',oldseg
                if (seg == oldseg):
                    #print ("    remove interior intersection",istart
                    seg0 = intersections[istart][0][SEG]
                    vert0 = intersections[istart][0][VERT]
                    path[seg0][vert0][INTERSECT] = -1
                    seg1 = intersections[istart][1][SEG]
                    vert1 = intersections[istart][1][VERT]
                    path[seg1][vert1][INTERSECT] = -1
                    intersections[istart] = []
                    break
                elif (seg == []):
                    seg = intersections[intersection][0][SEG]
                    vert = intersections[intersection][0][SEG]
                    oldseg = []
                else:
                    oldseg = seg
                    intersection = []
                    while (intersection == []):
                        if (vert < (len(path[seg])-1)):
                            vert += 1
                        else:
                            vert = 0
                        intersection = path[seg][vert][INTERSECT]
                    if (intersection == -1):
                        intersection = istart
                        break
                    elif (intersection == istart):
                        #print '    back to',istart
                        interior = FALSE
                        intersection = istart
                        break
            #
            # save path if valid boundary intersection
            #
            if (interior == FALSE):
                newseg = len(newpath)
                newpath.append([])
                while 1:
                    #print 'keeping intersection',intersection,':',intersections[intersection]
                    [seg,vert] = union(intersection,path,intersections,sign)
                    if (seg == []):
                        seg = intersections[intersection][0][SEG]
                        vert = intersections[intersection][0][VERT]
                    #print '  seg',seg,'vert',vert
                    intersections[intersection] = []
                    intersection = []
                    while (intersection == []):
                        if (vert < (len(path[seg])-1)):
                            x = path[seg][vert][X]
                            y = path[seg][vert][Y]
                            newpath[newseg].append([x,y,[]])
                            vert += 1
                        else:
                            vert = 0
                        intersection = path[seg][vert][INTERSECT]
                    if (intersection == istart):
                        #print '    back to',istart
                        x = path[seg][vert][X]
                        y = path[seg][vert][Y] 
                        newpath[newseg].append([x,y,[]])
                        break
            i += 1
    return newpath

def union_boundary(event):
    global boundary, intersections
    #
    # union intersecting polygons on boundary
    #
    print ("union boundary ...")
    sign = 1
    #boundary = prune(boundary,sign,event)
    boundary = new_prune(boundary,sign,event)
    print ("    done")
    plot(event)
    
def contour_boundary(event):
    global boundary, toolpath
    #
    # contour boundary to find toolpath
    #
    print ("contouring boundary ...")
    undercut = float(sundercut.get())
    if (undercut != 0.0):
        print ("    undercutting contour by",undercut)
    #
    # displace vertices inward by tool size
    #
        print ("    displacing ...")
        toolpath = displace(boundary)
    else:
        print ("     WARNING: no displacement set")
    plot(event)
    print('displaced')
    sign = -1
    #toolpath = new_prune(toolpath,sign,event)
    plot(event)
    print ("    done")

def raster(event):
    global boundary, toolpath, ymin, ymax
    #
    # raster interior
    #
    print ("rastering interior ...")
    scale = float(sscale.get())
    tooldia = float(sdia.get())/scale
    overlap = float(soverlap.get())
    if (toolpath == []):
        edgepath = boundary
        delta = tooldia/2.0
    else:
        edgepath = toolpath
        delta = tooldia/4.0
    #
    # find row-edge intersections
    #
    edges = []
    dymin = ymin - 2*tooldia*overlap
    dymax = ymax + 2*tooldia*overlap
    row1 = int(floor((dymax-dymin)/(tooldia*overlap)))
    for row in range(row1+1):
        edges.append([])
    for seg in range(len(edgepath)):
        for vertex in range(len(edgepath[seg])-1):
            x0 = edgepath[seg][vertex][X]
            y0 = edgepath[seg][vertex][Y]
            x1 = edgepath[seg][vertex+1][X]
            y1 = edgepath[seg][vertex+1][Y]
            if (y1 == y0):
                continue
            elif (y1 < y0):
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            row0 = int(ceil((y0 - dymin)/(tooldia*overlap)))
            row1 = int(floor((y1 - dymin)/(tooldia*overlap)))
            for row in range(row0,(row1+1)):
                y = dymin + row*tooldia*overlap
                x = x0*(y1-y)/(y1-y0) + x1*(y-y0)/(y1-y0)
                edges[row].append(x)
    for row in range(len(edges)):
        edges[row].sort()
        y = dymin + row*tooldia*overlap
        edge = 0
        while edge < len(edges[row]):
            x0 = edges[row][edge] + delta
            edge += 1
            if (edge < len(edges[row])):
                x1 = edges[row][edge] - delta
            else:
                print ("shouldn't happen: row",row,"length",len(edges[row]))
                break
            edge += 1
            if (x0 < x1):
                toolpath.append([])
                toolpath[-1].append([x0,y,[]])
                toolpath[-1].append([x1,y,[]])
    plot(event)
    print ("    done")

def write_RML(path):
    #
    # RML (Modela-style HPGL) output
    #
    units = 1000
    scale = float(sscale.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    text = outfile.get()
    izup = int(units*float(szup.get()))
    izdown = int(units*float(szdown.get()))
    file = open(text, 'w')
    file.write("PA;PA;!PZ"+str(izdown)+","+str(izup)+";")
    file.write("VS"+sxyvel.get()+";!VZ"+szvel.get()+";!MC1;")
    for segment in range(len(path)):
        vertex = 0
        x = int(units*(path[segment][vertex][X]*scale + xoff))
        y = int(units*(path[segment][vertex][Y]*scale + yoff))
        file.write("PU"+str(x)+","+str(y)+";")
        for vertex in range(1,len(path[segment])):
            x = int(units*(path[segment][vertex][X]*scale + xoff))
            y = int(units*(path[segment][vertex][Y]*scale + yoff))
            file.write("PD"+str(x)+","+str(y)+";")
    #file.write("PU5000,5000;!MC0;")
    file.write("PU"+str(x)+","+str(y)+";!MC0;")
    file.close()
    print ("wrote",len(path),"RML toolpath segments to",text)

def write_CAMM(path):
    #
    # CAMM (CAMM-style cutter HPGL) output
    #
    units = 1000
    scale = float(sscale.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    text = outfile.get()
    #izup = int(units*float(szup.get()))
    #izdown = int(units*float(szdown.get()))
    file = open(text, 'w')
    file.write("PA;PA;!ST1;!FS"+sforce.get()+";VS"+svel.get()+";")
    for segment in range(len(path)):
        vertex = 0
        x = int(units*(path[segment][vertex][X]*scale + xoff))
        y = int(units*(path[segment][vertex][Y]*scale + yoff))
        file.write("PU"+str(x)+","+str(y)+";")
        for vertex in range(1,len(path[segment])):
            x = int(units*(path[segment][vertex][X]*scale + xoff))
            y = int(units*(path[segment][vertex][Y]*scale + yoff))
            file.write("PD"+str(x)+","+str(y)+";")
    file.write("PU0,0;")
    file.close()
    print ("wrote",len(path),"CAMM toolpath segments to",text)

def write_EPI(path):
    #
    # Epilog lasercutter output
    #
    units = 1000
    scale = float(sscale.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    text = outfile.get()
    file = open(text, 'w')
    file.write("%-12345X@PJL JOB NAME=Graphic1\r\nE@PJL ENTER LANGUAGE=PCL\r\n&y1A&l0U&l0Z&u600D*p0X*p0Y*t600R*r0F&y50P&z50S*r6600T*r5100S*r1A*rC%1BIN;XR"+srate.get()+";YP"+spower.get()+";ZS"+sspeed.get()+";")
    for segment in range(len(path)):
        vertex = 0
        x = int(units*(path[segment][vertex][X]*scale + xoff))
        y = int(units*(path[segment][vertex][Y]*scale + yoff))
        file.write("PU"+str(x)+","+str(y)+";")
        for vertex in range(1,len(path[segment])):
            x = int(units*(path[segment][vertex][X]*scale + xoff))
            y = int(units*(path[segment][vertex][Y]*scale + yoff))
            file.write("PD"+str(x)+","+str(y)+";")
    file.write("%0B%1BPUE%-12345X@PJL EOJ \r\n")
    file.close()
    print ("wrote",len(path),"Epilog toolpath segments to",text)

def write_G(path):
    #
    # G code output
    #
    scale = float(sscale.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    text = outfile.get()
    file = open(text, 'w')
    file.write("G90\n") # absolute positioning
    file.write("F"+sfeed.get()+"\n") # feed rate
    file.write("S"+sspindle.get()+"\n") # spindle speed
    file.write("T"+stool.get()+"\n") # tool
    file.write("M08\n") # coolant on
    file.write("M03\n") # spindle on clockwise
    for segment in range(len(path)):
        vertex = 0
        x = path[segment][vertex][X]*scale + xoff
        y = path[segment][vertex][Y]*scale + yoff
        file.write("G00X%0.4f"%x+"Y%0.4f"%y+"Z"+sztop.get()+"\n") # rapid motion
        file.write("G01Z"+szbottom.get()+"\n") # linear motion
        for vertex in range(1,len(path[segment])):
            x = path[segment][vertex][X]*scale + xoff
            y = path[segment][vertex][Y]*scale + yoff
            file.write("X%0.4f"%x+"Y%0.4f"%y+"\n")
        file.write("Z"+sztop.get()+"\n")
    file.write("M05\n") # spindle stop
    file.write("M09\n") # coolant off
    file.write("M30\n") # program end and reset
    file.close()
    print ("wrote",len(path),"G code toolpath segments to",text)

def write_img(path):
    #
    # bitmap image output
    #
    text = 'wite image not implimented'
    '''
    scale = float(sscale.get())
    size = float(ssize.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    text = outfile.get()
    ximg = int(sximg.get())
    yimg = int(syimg.get())
    
    image = Image.new("RGB",[ximg,yimg],(0,0,0))
    draw = Image.Draw(image)
    for segment in range(len(path)):
        vertex = 0
        x0 = int((path[segment][vertex][X]*scale + xoff)*ximg/size)
        y0 = yimg - int((path[segment][vertex][Y]*scale + yoff)*yimg/size)
        for vertex in range(1,len(path[segment])):
            x1 = int((path[segment][vertex][X]*scale + xoff)*ximg/size)
            y1 = yimg - int((path[segment][vertex][Y]*scale + yoff)*yimg/size)
            draw.line([(x0,y0),(x1,y1)],(255,255,255))
            [x0,y0] = [x1,y1]
    image.save(text)
    '''
    print ("wrote",len(path),"toolpath segments to image",text)

def write_scad(path):
    #
    # scad script output
    #
    
    #scale = float(sscale.get())
    size = float(ssize.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    text = outfile.get()
    #ximg = int(sximg.get())
    #yimg = int(syimg.get())
    print ("Writing toolpath segments to OpenSCAD script file ",text)
    file = open(text, 'w')
    file.write("// SCAD file generated by TGrosch python script" + DATE +"\n") # header
    file.write("//    xoffset " + str(gscale*xoff) + "\n") # absolute x positioning
    file.write("//    yoffset " + str(gscale*yoff) + "\n") # absolute y positioning
    file.write("//    \n")
    file.write ("module path() {\n")
    for i in range(len(path)):
        file.write("// poth " + str(i) + "\n") 
        file.write("    a"+str(i)+" = [") 
        for j in range(len(path[i])-1):
            file.write("["+str(gscale*path[i][j][0])+","+str(gscale*path[i][j][1])+"]" )
            file.write(",")   
        file.write("["+str(gscale*path[i][0][0])+","+str(gscale*path[i][0][1])+"]];\n" )
        #file.write("    b = [[") 
        #for j in range(len(path[i])-1):  
        #    file.write(str(j)+",")
        #file.write(str(j+1)+"]];\n")
        file.write("polygon(a"+str(i)+");\n")
    file.write ("}\n linear_extrude(height = "+str(gscale*mthickness)+", center = true, convexity = 10, twist = 0) path();\n")
    file.close()
    print ("wrote",len(path),"toolpath segments to scad file",text)

def write_via_scad(vias):
    #
    # scad script output
    #
    global sthickness, mthickness, mwidth, gscale
    #scale = float(sscale.get())
    size = float(ssize.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    text = outfile.get()
    #index = text.find(".")
    #text = text[0:index]+"Drill.scad"
    
    h1 = gscale * sthickness + mthickness
    #ximg = int(sximg.get())
    #yimg = int(syimg.get())
    print ("Writing vias to OpenSCAD script file ",text)
    file = open(text, 'w')
    file.write("// SCAD file generated by TGrosch python script" + DATE +"\n") # header
    file.write("//    xoffset " + str(gscale*xoff) + "\n") # absolute x positioning
    file.write("//    yoffset " + str(gscale*yoff) + "\n") # absolute y positioning
    file.write("//    \n")
    file.write ("module drills() {\n")
    for i in range(len(vias)):
        x0 = gscale * vias[i][0][0]
        y0 = gscale * vias[i][0][1]
        r1 = gscale * vias[i][0][2]/2.
        file.write("    translate (["+str(x0)+","+str(y0)+",0]) cylinder("+str(h1)+","+str(r1)+","+str(r1)+",center=true,$fn=50);\n") 
    file.write("}\n")
    file.write("module voids() {\n")  
    w = 2*mwidth;
    for i in range(len(vias)):
        if (vias[i][0][2] > w):
            x0 = gscale * vias[i][0][0];
            y0 = gscale * vias[i][0][1];
            r1 = (gscale * vias[i][0][2]/2.) - 2*mthickness;
            file.write("    translate (["+str(x0)+","+str(y0)+",0]) cylinder("+str(h1+.1)+","+str(r1)+","+str(r1)+",center=true,$fn=50);\n") 
    file.write ("}\n")
    file.write("module vias() {\n")
    file.write("    difference () {\n")
    file.write("        drills();\n")
    file.write("        voids();\n")
    file.write("     }\n")
    file.write("}\n")
    file.write("vias();")
    file.close()
    print ("wrote",len(vias),"via holes to scad file",text)

def write_outline_scad(path):
    #
    # scad script output
    #
    #scale = float(sscale.get())
    size = float(ssize.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    text = outfile.get()
    x0min = HUGE
    x0max = -HUGE
    y0min = HUGE
    y0max = -HUGE
    #ximg = int(sximg.get())
    #yimg = int(syimg.get())
    print ("Writing toolpath segments to OpenSCAD script file ",text)
    file = open(text, 'w')
    file.write("// SCAD file generated by TGrosch python script" + DATE +"\n") # header
    file.write("//    xoffset " + str(gscale*xoff) + "\n") # absolute x positioning
    file.write("//    yoffset " + str(gscale*yoff) + "\n") # absolute y positioning
    file.write("//    \n")
    file.write ("module path() {\n")
    for i in range(len(path)):
        file.write("// poth " + str(i) + "\n") 
        file.write("    a"+str(i)+" = [") 
        for j in range(len(path[i])):
            x0 = gscale*path[i][j][0]
            y0 = gscale*path[i][j][1]
            file.write("["+str(x0)+","+str(y0)+"]" )
            file.write(",")
            if (x0 > x0max):
                x0max = x0;
            elif (x0 < x0min):
                x0min = x0 
            if (y0 > y0max):
                y0max = y0
            elif(y0 < y0min):
                y0min = y0
        file.write("["+str(gscale*path[i][0][0])+","+str(gscale*path[i][0][1])+"]];\n" )
        #file.write("    b = [[") 
        #for j in range(len(path[i])-1):  
        #    file.write(str(j)+",")
        #file.write(str(j+1)+"]];\n")
        file.write("polygon(a"+str(i)+");\n")
    file.write("}\n")
    file.write("module substrate() {\n")
    file.write("    difference() {\n")
    file.write("       translate(["+str((x0max + x0min)/2)+","+str((y0max + y0min)/2)+",0]) cube(["+str((x0max - x0min))+","+str((y0max - y0min))+","+str(gscale*mthickness)+"], center = true);\n")
    file.write("       linear_extrude(height = "+str(gscale*mthickness+.1)+", center = false, convexity = 10, twist = 0) path();\n")
    file.write("    }\n")
    file.write("} substrate();\n")
    file.close()
    print ("wrote",len(path),"toolpath segments to scad file",text)


def write(event):
    global toolpath, boundary, vias, xmin, xmax, ymin, ymax, gscale
    #
    # write toolpath
    #
    if (toolpath == []):
        toolpath = boundary
    texti = infile.get()
    text = outfile.get()
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
    elif (text.find(".scad") != -1 ):
        if (texti.find(".drl") != -1):
            write_via_scad(vias)
        elif(texti.find(".otl") != -1):
            write_outline_scad(toolpath)
        else:
            write_scad(toolpath)

    else:
        print ("unsupported output file format")
        return
    sxmin = gscale * (xmin + xoff)
    sxmax = gscale * (xmax + xoff)
    symin = gscale * (ymin + yoff)
    symax = gscale * (ymax + yoff)
    print ("    xmin: %0.3g "%sxmin,"xmax: %0.3g "%sxmax,"ymin: %0.3g "%symin,"ymax: %0.3g "%symax)

def delframes():
    #
    # delete all CAM frames
    #
    global cutframe, imgframe, toolframe, millframe, gframe,laserframe
    cutframe.pack_forget()
    imgframe.pack_forget()
    toolframe.pack_forget()
    millframe.pack_forget()
    gframe.pack_forget()
    laserframe.pack_forget()

def camselect(event):
    global size
    #
    # pack appropriate CAM GUI options based on output file
    #
    global outfile, soverlap, szup, szdown, sxyvel, szvel, sforce, svel, srate, spower, sspeed, sztop, szbottom, sfeed, sspindle, stool, sximg, syimg
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
        print ("output file format not supported")
    return

root = tk.Tk()
root.title('cam.py')
root.bind('q','exit')

infile = tk.StringVar()
outfile = tk.StringVar()
if (len(sys.argv) >= 2):
    infile.set(sys.argv[1])
else:
    infile.set('')
if (len(sys.argv) >= 4):
    xoff = float(sys.argv[2])
    yoff = float(sys.argv[3])
if (len(sys.argv) >= 5):
    size = float(sys.argv[4])
if (len(sys.argv) >= 6):
    outfile.set(sys.argv[5])
else:
    outfile.set('out.rml')
if (len(sys.argv) >= 7):
    undercut = float(sys.argv[6])
    
inframe = tk.Frame(root)
tk.Label(inframe, text="input file: ").pack(side="left")
winfile = tk.Entry(inframe, width=20, textvariable=infile)
winfile.pack(side="left")
winfile.bind('<Return>',read)
ssize = tk.StringVar()
ssize.set(str(size))
tk.Label(inframe, text=" ").pack(side="left")
tk.Label(inframe, text="display size:").pack(side="left")
wsize = tk.Entry(inframe, width=10, textvariable=ssize)
wsize.pack(side="left")
wsize.bind('<Return>',plot)
tk.Label(inframe, text=" ").pack(side="left")
ivert = tk.IntVar()
wvert = tk.Checkbutton(inframe, text="show vertices", variable=ivert)
wvert.pack(side="left")
#wvert.bind('<tk.ButtonRelease-1>',plot)
inframe.pack()

coordframe = tk.Frame(root)
sxoff = tk.StringVar()
sxoff.set(str(xoff))
syoff = tk.StringVar()
syoff.set(str(yoff))
sscale = tk.StringVar()
sscale.set(str(scale))
tk.Label(coordframe, text="x offset:").pack(side="left")
wxoff = tk.Entry(coordframe, width=10, textvariable=sxoff)
wxoff.pack(side="left")
wxoff.bind('<Return>',plot)
tk.Label(coordframe, text=" y offset:").pack(side="left")
wyoff = tk.Entry(coordframe, width=10, textvariable=syoff)
wyoff.pack(side="left")
wyoff.bind('<Return>',plot)
tk.Label(coordframe, text=" part scale factor:").pack(side="left")
wscale = tk.Entry(coordframe, width=10, textvariable=sscale)
wscale.pack(side="left")
wscale.bind('<Return>',plot_delete)
coordframe.pack()

c = tk.Canvas(root, width=WINDOW, height=WINDOW, background='white')
c.pack()

outframe = tk.Frame(root)

Logo = tk.Canvas(outframe, width=26, height=26, background="white")
Logo.create_oval(2,2,8,8,fill="red",outline="")
Logo.create_rectangle(11,2,17,8,fill="blue",outline="")
Logo.create_rectangle(20,2,26,8,fill="blue",outline="")
Logo.create_rectangle(2,11,8,17,fill="blue",outline="")
Logo.create_oval(10,10,16,16,fill="red",outline="")
Logo.create_rectangle(20,11,26,17,fill="blue",outline="")
Logo.create_rectangle(2,20,8,26,fill="blue",outline="")
Logo.create_rectangle(11,20,17,26,fill="blue",outline="")
Logo.create_rectangle(20,20,26,26,fill="blue",outline="")
Logo.pack(side="left")
status = tk.StringVar()
namedate = "    cam.py ("+DATE+")  "
status.set(namedate)
tk.Label(outframe, textvariable=status).pack(side="left")
tk.Label(outframe, text="output file: ").pack(side="left")
woutfile = tk.Entry(outframe, width=20, textvariable=outfile)
woutfile.bind('<Return>',camselect)
woutfile.pack(side="left")
tk.Label(outframe, text=" ").pack(side="left")
tk.Button(outframe, text="quit", command='exit').pack(side="left")
tk.Label(outframe, text=" ").pack(side="left")
outframe.pack()

camframe = tk.Frame(root)
unionbtn = tk.Button(camframe, text="union polygons")
unionbtn.bind('<Button-1>',union_boundary)
unionbtn.pack(side="left")
tk.Label(camframe, text=" ").pack(side="left")
contourbtn = tk.Button(camframe, text="contour boundary")
contourbtn.bind('<Button-1>',contour_boundary)
contourbtn.pack(side="left")
tk.Label(camframe, text=" ").pack(side="left")
rasterbtn = tk.Button(camframe, text="raster interior")
rasterbtn.bind('<Button-1>',raster)
rasterbtn.pack(side="left")
tk.Label(camframe, text=" ").pack(side="left")
writebtn = tk.Button(camframe, text="write toolpath")
writebtn.bind('<Button-1>',write)
writebtn.pack(side="left")
camframe.pack()

toolframe = tk.Frame(root)
tk.Label(toolframe, text="tool diameter: ").pack(side="left")
sdia = tk.StringVar()
wtooldia = tk.Entry(toolframe, width=10, textvariable=sdia)
wtooldia.pack(side="left")
wtooldia.bind('<Return>',plot_delete)
tk.Label(toolframe, text=" contour undercut: ").pack(side="left")
sundercut = tk.StringVar()
wundercut = tk.Entry(toolframe, width=10, textvariable=sundercut)
wundercut.pack(side="left")
wundercut.bind('<Return>',plot_delete)
tk.Label(toolframe, text=" raster overlap: ").pack(side="left")
soverlap = tk.StringVar()
woverlap = tk.Entry(toolframe, width=10, textvariable=soverlap)
woverlap.pack(side="left")
woverlap.bind('<Return>',plot_delete)

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