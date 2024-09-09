'''
Created on Apr 2, 2017

@author: tedgrosch

This script converts a stack of gerber files and excellon drill file to gcode for PDB printer

Process:
    Open txt file that has 
        comments that begin with #
        a list of printer settings ie. oddset, speeds, layer thickess etc
        a list of layers in order from bottom to top and drill file last
    Read file names
    read drill file
        Create a insulating inner and top layer toolpath
        Create a via hole layer toolpath
    Write G-code header 
    Write Gcode for lower insulating layer with holes
        union of insulating layer and condutor oas unfilled layer
    Read bottom gerber file
        create a toolpath
        write gcode segment for bottom layer
    Write Gcode via hole conductor as unfilled circles
    Write Gcode for insulating layer
    while (!top layer)
        Read next layer is layer top?
            create a toolpath
            write gcode segment for this layer
        Write Gcode via hole conductor as unfilled circles
        Write Gcode for insulating layer
    Home tool
    close files

    
'''
DATE = "11/9/03"
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
scale = 1.0  # scale PCB if necessary
undercut = 0.0
sdia = 0.015
soverlap = 0.8
Xsize = 200 # printer size in mm
Ysize = 200 # printer y size in mm
Xmin = 0 # lower corner of rboard
Ymin = 0
Xmax = 10 #upper corner of board
Ymax = 10 
xoff = Xsize/2 # xoffset to center of print
yoff = Ysize/2 # y offset tot center of print 
subthick = 1.0; # substarte thickness in mm
xyres = 0.4 # x-y resolution
zres = 0.2 # z resolution
zlayers = 10 # number of z-layers thickness = zlayer*zres
Erate = 2 #extrusion rate in mm per mm
feed = 3.00 
spindle = 5000 
tool = 1
ztop = 1 
zbottom = 0

boundary = []
toolpath = []
itoolpath = []

HUGE = 1e10
xmin = HUGE
xmax = -HUGE
ymin = HUGE
ymax = -HUGE
Xmin = HUGE # lower corner of rboard
Ymin = HUGE
Xmax = -HUGE #upper corner of board
Ymax = -HUGE


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
UNITS = "MM"

#from Tkinter import *
from string import *
from math import *
from random import *
import sys #, Image, ImageDraw - commented out until the tutorial will be fixed to include these
##mport tkinter as tk

def stroke(x0,y0,x1,y1,width):
    #
    # stroke segment with width
    #
    #print "stroke:",x0,y0,x1,y1,width
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
    for i in range(NVERTS/2):
        newpath.append([x0+dx,y0+dy,0])
        [dx,dy] = [c*dx-s*dy, s*dx+c*dy]
        dx = dxperp * width/2.0
        dy = dyperp * width/2.0
    for i in range(NVERTS/2):
        newpath.append([x1+dx,y1+dy,0])
        [dx,dy] = [c*dx-s*dy, s*dx+c*dy]
        x0 = newpath[0][X]
        y0 = newpath[0][Y]
    newpath.append([x0,y0,0])
    return newpath

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
        y = int(str[(yindex+1):index])*(10**(-fraction))
    elif (yindex == -1):
        y = gerby
        x = int(str[(xindex+1):index])*(10**(-fraction))
    else:
        x = int(str[(xindex+1):yindex])*(10**(-fraction))
        y = int(str[(yindex+1):index])*(10**(-fraction))
    gerbx = x
    gerby = y
    return [x,y]


def read_Gerber(tstr):
    #
    # Gerber parser
    #
    segment = -1
    xold = []
    yold = []
    line = 0
    filelines = tstr.split('\n')
    nlines = len(filelines)
    path = []
    apertures = []
    macros = []
    N_macros = 0
    for i in range(100):
        apertures.append([])
    while line < nlines:
        if (filelines[line].find("%FS") != -1):
            #
            # format statement
            #
            index = filelines[line].find("X")
            digits = int(filelines[line][index+1])
            fraction = int(filelines[line][index+2])
            line += 1
            continue
        elif (filelines[line].find("%AM") != -1):
            #
            # aperture macro
            #
            index = filelines[line].find("%AM")
            index1 = filelines[line].find("*")
            macros.append([])
            macros[-1] = filelines[line][index+3:index1]
            N_macros += 1
            line += 1
            continue
        elif (filelines[line].find("%ADD") != -1):
            #
            # aperture definition
            #
            index = filelines[line].find("%ADD")
            parse = 0
            if (filelines[line].find("C,") != -1):
                #
                # circle
                #
                index = filelines[line].find("C,")
                index1 = filelines[line].find("*")
                aperture = int(filelines[line][4:index])
                size = float(filelines[line][index+2:index1])
                apertures[aperture] = ["C",size]
                print ("   read aperture",aperture,": circle diameter",size)
                line += 1
                continue
            elif (filelines[line].find("O,") != -1):
                #
                # obround
                #
                index = filelines[line].find("O,")
                aperture = int(filelines[line][4:index])
                index1 = filelines[line].find(",",index)
                index2 = filelines[line].find("X",index)
                index3 = filelines[line].find("*",index)
                width = float(filelines[line][index1+1:index2])
                height = float(filelines[line][index2+1:index3])
                apertures[aperture] = ["O",width,height]
                print ("   read aperture",aperture,": obround",width,"x",height)
                line += 1
                continue
            elif (filelines[line].find("R,") != -1):
                #
                # rectangle
                #
                index = filelines[line].find("R,")
                aperture = int(filelines[line][4:index])
                index1 = filelines[line].find(",",index)
                index2 = filelines[line].find("X",index)
                index3 = filelines[line].find("*",index)
                width = float(filelines[line][index1+1:index2])
                height = float(filelines[line][index2+1:index3])
                apertures[aperture] = ["R",width,height]
                print ("   read aperture",aperture,": rectangle",width,"x",height)
                line += 1
                continue
            for macro in range(N_macros):
                #
                # macros
                #
                index = filelines[line].find(macros[macro]+',')
                if (index != -1):
                    #
                    # hack: assume macros can be approximated by
                    # a circle, and has a size parameter
                    #
                    aperture = int(filelines[line][4:index])
                    index1 = filelines[line].find(",",index)
                    index2 = filelines[line].find("*",index)
                    size = float(filelines[line][index1+1:index2])
                    apertures[aperture] = ["C",size]
                    print ("   read aperture",aperture,": macro (assuming circle) diameter",size)
                    parse = 1
                    continue
            if (parse == 0):
                print ("  aperture not implemented:",filelines[line])
                return
        elif (filelines[line].find("D") == 0):
            #
            # change aperture
            #
            index = filelines[line].find('*')
            aperture = int(filelines[line][1:index])
            size = apertures[aperture][SIZE]
            line += 1
            continue
        elif (filelines[line].find("G54D") == 0):
            #
            # change aperture
            #
            index = filelines[line].find('*')
            aperture = int(filelines[line][4:index])
            size = apertures[aperture][SIZE]
            line += 1
            continue
        elif (filelines[line].find("D01*") != -1):
            #
            # pen down
            #
            [xnew,ynew] = coord(filelines[line],digits,fraction)
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
        elif (filelines[line].find("D02*") != -1):
            #
            # pen up
            #
            [xold,yold] = coord(filelines[line],digits,fraction)
            if (size < EPS):
                path.append([])
                segment += 1
                path[segment].append([xold,yold,[]])
            newpath = []
            line += 1
            continue
        elif (filelines[line].find("D03*") != -1):
            #
            # flash
            #
            [xnew,ynew] = coord(str[line],digits,fraction)
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
                #    rectangle
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
                print ("   aperture",apertures[aperture][TYPE],"is not implemented")
                return
            xold = xnew
            yold = ynew
            continue
        else:
            print ("   not parsed:",str[line])
        line += 1
    return path

def read_Excellon(tstr):
    #
    # Excellon parser
    #
    segment = -1
    line = 0
    filelines = tstr.split('\n')
    nlines = len(filelines)
    path = []
    drills = []
    header = FALSE
    for i in range(100):
        drills.append([])
    while line < nlines:
        if ((filelines[line].find("T") != -1) & (filelines[line].find("C") != -1) & (filelines[line].find("F") != -1)):
            #
            # alternate drill definition style
            #
            index = filelines[line].find("T")
            index1 = filelines[line].find("C")
            index2 = filelines[line].find("F")
            drill = int(filelines[line][1:index1])
            print (filelines[line][index1+1:index2])
            size = float(filelines[line][index1+1:index2])
            drills[drill] = ["C",size]
            print ("   read drill",drill,"size:",size)
            line += 1
            continue
        if ((filelines[line].find("T") != -1) & (filelines[line].find(" ") != -1) & (filelines[line].find("in") != -1)):
            #
            # alternate drill definition style
            #
            index = filelines[line].find("T")
            index1 = filelines[line].find(" ")
            index2 = filelines[line].find("in")
            drill = int(filelines[line][1:index1])
            print (filelines[line][index1+1:index2])
            size = float(filelines[line][index1+1:index2])
            drills[drill] = ["C",size]
            print ("   read drill",drill,"size:",size)
            line += 1
            continue
        elif ((filelines[line].find("T") != -1) & (filelines[line].find("C") != -1)):
            #
            # alternate drill definition style
            #
            index = filelines[line].find("T")
            index1 = filelines[line].find("C")
            drill = int(filelines[line][1:index1])
            size = float(filelines[line][index1+1:-1])
            drills[drill] = ["C",size]
            print ("   read drill",drill,"size:",size)
            line += 1
            continue
        elif (filelines[line].find("T") == 0):
            #
            # change drill
            #
            #index = filelines[line].find('T')
            drill = int(filelines[line].strip('T'))
            size = drills[drill][SIZE]
            if (UNITS == 'INCH'):
                size /= 25.4
            line += 1
            continue
        elif (filelines[line].find("M") != -1):
            #
            # Parse commands
            #
            temp=filelines[line].strip("M")
            if (int(temp) == 48):
                header = FALSE
                print("Drill fiel headder found")

            if (int(temp) == 72):
                UNITS = "INCH";
                print("Units are set to INCH")
            elif (int(temp) == 71):
                UNITS = "MM";
                print("Units were set to MM'")
            else:
                print ("   not parsed:",filelines[line])
            line += 1
            continue
        elif (filelines[line].find("X") != -1):
            #
            # drill location
            #
            index = filelines[line].find("X")
            index1 = filelines[line].find("Y")
            x0 = float(int(filelines[line][index+1:index1])/1000.0)
            y0 = float(int(filelines[line][index1+1:])/1000.0)
            if (UNITS == 'INCH'):
                x0 /= 25.4
                y0 /= 25.4
            line += 1
            path.append([])
            segment += 1    
            size = drills[drill][SIZE] - xyres #make drill smaller by thickness of line
            # clculate NVERTS based on the size of the drill bit and with of conductoer
            nverts = (round(size/xyres)+1)
            for i in range(NVERTS):
                angle = -i*2.0*pi/(NVERTS-1.0)
                x = x0 + (size/2.0)*cos(angle)
                y = y0 + (size/2.0)*sin(angle)
                path[segment].append([x,y,[]])
            continue
        elif (filelines[line].find("INCH") != -1):
                UNITS = "INCH";
                print("Units are set to INCH")
        elif (filelines[line].find("METRIC") != -1):
                UNITS = "MM";
                print("Units were set to MM'")
        else:
            print ("   not parsed:",filelines[line])
        line += 1
    return path

def intersect(path,seg0,vert0,sega,verta):
    #
    # test and return edge intersection
    #
    if ((seg0 == sega) & (vert0 == 0) & (verta == (len(path[sega])-2))):
        #print "   return (0-end)"
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
        #print "zero-length segment"
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
        #print " same side"
        return [[],[]]
    elif ((abs(dperp0a) < EPS) & (abs(dperp0b) < EPS)):
        #
        # edges colinear, return no intersection
        #
        #d0a = (xa-x0)*dxpar01 + (ya-y0)*dypar01
        #d0b = (xb-x0)*dxpar01 + (yb-y0)*dypar01
        #print " colinear"
        return [[],[]]
    #
    # calculation distance to intersection
    #
    d = (dpar0a*abs(dperp0b)+dpar0b*abs(dperp0a))/(abs(dperp0a)+abs(dperp0b))
    if ((d < -EPS) | (d > (d01+EPS))):
        #
        # intersection outside segment, return no intersection
        #
        #print "   found intersection outside segment"
        return [[],[]]
    else:
        #
        # intersection in segment, return intersection
        #
        #print "   found intersection in segment s0 v0 sa va",seg0,vert0,sega,verta
        xloc = x0 + dxpar01*d
        yloc = y0 + dypar01*d
        return [xloc,yloc]

def union(i,path,intersections,sign):
    #
    # return edge to exit intersection i for a union
    #
    #print "union: intersection",i,"in",intersections
    seg0 = intersections[i][0][SEG]
    #print "seg0",seg0
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
    #print "   dot",dot
    if (abs(dot) <= EPS):
        print ("  colinear")
        seg = []
        vert= []
    elif (dot > EPS):
        seg = intersections[i][(1-sign)/2][SEG]
        vert = intersections[i][(1-sign)/2][VERT]
    else:
        seg = intersections[i][(1+sign)/2][SEG]
        vert = intersections[i][(1+sign)/2][VERT]
    return [seg,vert]


def insert(path,x,y,seg,vert,intersection):
    #
    # insert a vertex at x,y in seg,vert, if needed
    #
    d0 = (path[seg][vert][X]-x)**2 + (path[seg][vert][Y]-y)**2
    d1 = (path[seg][vert+1][X]-x)**2 + (path[seg][vert+1][Y]-y)**2
    #print "check insert seg",seg,"vert",vert,"intersection",intersection
    if ((d0 > EPS) & (d1 > EPS)):
        #print "   added intersection vertex",vert+1
        path[seg].insert((vert+1),[x,y,intersection])
        return 1
    elif (d0 < EPS):
        if (path[seg][vert][INTERSECT] == []):
            path[seg][vert][INTERSECT] = intersection
            #print "   added d0",vert
        return 0
    elif (d1 < EPS):
        if (path[seg][vert+1][INTERSECT] == []):
            path[seg][vert+1][INTERSECT] = intersection
            #print "   added d1",vert+1
        return 0
    else:
        #print "   shouldn't happen: d0",d0,"d1",d1
        return 0



def add_intersections(path):
    #
    # add vertices at path intersections
    #
    intersection = 0
    #
    # loop over first edge
    #
    for seg0 in range(len(path)):
        #status.set("   segment "+str(seg0)+"/"+str(len(path)-1)+"  ")
        #outframe.update()
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
    #status.set(namedate)
    #outframe.update()
    intersections = []
    for i in range(intersection): intersections.append([])
    for seg in range(len(path)):
        for vert in range(len(path[seg])):
            intersection = path[seg][vert][INTERSECT]
        if (intersection != []):
            intersections[intersection].append([seg,vert])
    #print '   found',len(intersections),'intersection(s)'
    seg_intersections = []
    for i in range(len(path)): seg_intersections.append([])
    for i in range(len(intersections)):
        if (len(intersections[i]) != 2):
            print ("   shouldn't happen: i",i,intersections[i])
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
    dx1par = dx0 / d1
    dy1par = dy0 / d1

    dx0perp = dy0 / d0
    dy0perp = -dx0 / d0
    dx1perp = dy1 / d1
    dy1perp = -dx1 / d1
    #print "offset points:",x0,x1,x2,y0,y1,y2
    #print "offset normals:",dx0perp,dx1perp,dy0perp,dy1perp
    if ((abs(dx0perp*dy1perp - dx1perp*dy0perp) < EPS) | (abs(dy0perp*dx1perp - dy1perp*dx0perp) < EPS)):
        dx = r * dx1perp
        dy = r * dy1perp
        #print "   offset planar:",dx,dy
    elif ((abs(dx0perp+dx1perp) < EPS) & (abs(dy0perp+dy1perp) < EPS)):
        dx = r * dx1par
        dy = r * dy1par
        #print "   offset hairpin:",dx,dy
    else:
        dx = r*(dy1perp - dy0perp)  / \
            (dx0perp*dy1perp - dx1perp*dy0perp)
        dy = r*(dx1perp - dx0perp) / \
            (dy0perp*dx1perp - dy1perp*dx0perp)
            #print "   offset OK:",dx,dy
    return [dx,dy]



def displace(path):
    #
    # displace path inwards by tool radius
    #
    global scale, sundercut, sdia
    newpath = []
    #scale = float(sscale.get())
    undercut = sundercut
    toolrad = sdia
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
            x0 = newpath[seg][0][X]
            y0 = newpath[seg][0][Y]
            newpath[seg].append([x0,y0,[]])
        elif (len(path[seg]) == 2):
            x0 = path[seg][0][X]
            y0 = path[seg][0][Y]
            x1 = path[seg][1][X]
            y1 = path[seg][1][Y]
            x2 = 2*x1 - x0
            y2 = 2*y1 - y0
            [dx,dy] = offset(x0,x1,x2,y0,y1,y2,toolrad)
            if (dx != []):
                newpath[seg].append([x0+dx,y0+dy,[]])
                newpath[seg].append([x1+dx,y1+dy,[]])
            else:
                newpath[seg].append([x0,y0,[]])
                newpath[seg].append([x1,y1,[]])
        else:
            print ("  displace: shouldn't happen")
    return newpath

def prune(path,sign,event):
    #
    # prune path intersections
    #
    # first find the intersections
    #
    print ("   intersecting ...")
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
    print ("   pruning ...")
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
                seg == oldseg
            else:
                [seg,vert] = union(intersection,path,intersections,sign)
                #print '  seg',seg,'vert',vert,'oldseg',oldseg
                if (seg == oldseg):
                    #print "   remove interior intersection",istart
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
                    #print '   back to',istart
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
                    #print '   back to',istart
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
    boundary = prune(boundary,sign,event)
    print ("   done")
    return

def contour_boundary(event):
    global boundary, toolpath, undercut
    #
    # contour boundary to find toolpath
    #
    print ("contouring boundary ...")
    #undercut = float(sundercut.get())
    if (undercut != 0.0):
        print ("   undercutting contour by",undercut)
    #
    # displace vertices inward by tool size
    #
    print ("   displacing ...")
    toolpath = displace(boundary)
    #plot_path(event)
    #raw_input('displaced')
    sign = -1
    toolpath = prune(toolpath,sign,event)
    #plot(event)
    print ("   done")

def raster(event):
    global boundary, toolpath, ymin, ymax
    #
    # raster interior
    #
    global scale, sdia, soverlap
    print ("rastering interior ...")
    tooldia = sdia
    overlap = soverlap
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
    #plot(event)
    print ("   done")


def read_Outline(tstr):
    #
    # Excellon parser
    #
    global Xmin, Ymin, Xmax, Ymax 
    filelines = tstr.split('\n')
    nlines = len(filelines)
    for line in range(0, nlines-1):
        temp = filelines[line]
        if (filelines[line].find("%FS") != -1):
            #
            # format statement
            #
            index = filelines[line].find("X")
            digits = int(filelines[line][index+1])
            fraction = int(filelines[line][index+2])
            scale = 1/(10**fraction)
        elif (filelines[line][0] == 'X'):
            #
            # find the min and max bord dimensions
            #
            index1 = filelines[line].find('X')
            index2 = filelines[line].find('Y')
            xdim = scale*float(filelines[line][index1+1:index1+digits+fraction+1])
            ydim = scale*float(filelines[line][index2+1:index2+digits+fraction+1])
            if (xdim < Xmin):
                Xmin = xdim
            if (ydim < Ymin):
                Ymin = ydim
            if (xdim > Xmax):
                Xmax = xdim
            if (ydim > Ymax):
                Ymax = ydim
        #else: do nothing 
    print ('Board outline found Xmin=',Xmin,' Ymin=',Ymin,'Xmax=',Xmax,"Yman=",Ymax)            
    return         
'''
def plot(event):
   global boundary, toolpath
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

  '''          
def write_G(path):
    #
    # G code output
    #
    global scale, xoff, yoff, feed, spindle, tool, Ztop, zbottom
    #scale = float(sscale.get())
    #xoff = float(sxoff.get())
    #yoff = float(syoff.get())
    text = outfile.get()
    file = open(text, 'w')
    file.write("G90\n") # absolute positioning
    file.write("F"+feed+"\n") # feed rate
    file.write("S"+spindle+"\n") # spindle speed
    file.write("T"+tool+"\n") # tool
    file.write("M08\n") # coolant on
    file.write("M03\n") # spindle on clockwise
    for segment in range(len(path)):
        vertex = 0
        x = path[segment][vertex][X]*scale + xoff
        y = path[segment][vertex][Y]*scale + yoff
        file.write("G00X%0.4f"%x+"Y%0.4f"%y+"Z"+ztop+"\n") # rapid motion
        file.write("G01Z"+zbottom+"\n") # linear motion
        for vertex in range(1,len(path[segment])):
            x = path[segment][vertex][X]*scale + xoff
            y = path[segment][vertex][Y]*scale + yoff
            file.write("X%0.4f"%x+"Y%0.4f"%y+"\n")
        file.write("Z"+ztop+"\n")
    file.write("M05\n") # spindle stop
    file.write("M09\n") # coolant off
    file.write("M30\n") # program end and reset
    file.close()
    print ("wrote",len(path),"G code toolpath segments to",text)


def write_solidlayer(Fout):
    #
    #
    #
    global Xsize , Ysize, Xmin , Ymin, Xmax, Ymax, zres, Erate
    Xl = Xsize/2 - (Xmax-Xmin)/2 #lower X corner
    Yl = Ysize/2 - (Ymax-Ymin)/2 #lower Y corner
    Xu = Xsize/2 + (Xmax-Xmin)/2 #lower X corner
    Yu = Ysize/2 + (Ymax-Ymin)/2 #lower Y corner
    xstart = Xl
    xstop = Xl
    ystart = Yl
    ystart = Yl;
    xstop = xmax
    ystop = Yl;
    Fout.write('G92 E0') 
    Fout.write('G1 X',xstart," Y",ystart," F7500\n") #mve nozel to lower corner
    zstart = zres
    Fout.write('G1 Z%7.3' % zres,' F7800.000') # poition nozel
    for ii in range(0,zlayers-1):
        #draw edge at slower speed
        #calculate extrusion speed
        Extr = Erate*sqrt(float((xstop-xstart)**2 + (ystop-ystart)**2))
        Fout.write('G1 X%7.3' % Xl," Y%7.3" % Yl," E%7.3" % Extr," F900\n")
        
    return
def write_conduction(Fout):
    return
    
def write_interlayer(Fout):
    return
          
            
if (len(sys.argv) >= 2):
    infile = sys.argv[1]
else:
    print ("ERROR: No inout file entered.")
    print ("Usage is GTG.py infile <xoff> <yoff> <size> <outfile> <undercut>")
    print("    where infile is a txt file of PCB layers from bottom to top and drill file")
    exit
if (len(sys.argv) >= 4):
    xoff = float(sys.argv[2])
    yoff = float(sys.argv[3])
if (len(sys.argv) >= 5):
    size = float(sys.argv[4])
if (len(sys.argv) >= 6):
    outfile = sys.argv[5]
else:
    outfile = 'out.gcode'
if (len(sys.argv) >= 7):
    undercut = float(sys.argv[6])
F = open(infile,'r')
# check for errors
files = F.read()
filelist = files.split('\n')
F.close()
# first file should be the drill file and find the drill file 
if (filelist[0].split('.',1)[-1]  != 'drd'):
    print ("ERROR: Drill file is not the first file in the list")
    quit()
drillfile = filelist[0].rstrip('\n')
print ("Drill file found %s" % drillfile)
F = open(drillfile,'r')
tstr = F.read()
drillpath = read_Excellon(tstr)
F.close();
# open otline file .otl
if (filelist[1].split('.',1)[-1]  != 'otl'):
    print ("ERROR: Outline file is not the second file in the list")
    quit()
outlinefile = filelist[1].rstrip('\n')
print ("Outline file found %s" % drillfile)
F = open(outlinefile,'r')
tstr = F.read()
read_Outline(tstr)
F.close();
# 
# Open gcode file for writing and write header
#
Fout = open(outfile,'w')
Fout.write("; generated by Gerber-to-Gcode ver 0.1" + DATE + "\n")
Fout.write("\n")
Fout.write("; external perimeters extrusion width = 0.50mm\n")
Fout.write("; perimeters extrusion width = 0.72mm\n")
Fout.write("; infill extrusion width = 0.72mm\n")
Fout.write("; solid infill extrusion width = 0.72mm\n")
Fout.write("; top infill extrusion width = 0.72mm\n")
Fout.write("\n")
Fout.write("M107\n")
Fout.write("M104 S200 ; set temperature\n")
Fout.write("G28 ; home all axes\n")
Fout.write("G1 Z5 F5000 ; lift nozzle\n")
Fout.write("\n")
Fout.write("M109 S200 ; wait for temperature to be reached\n")
Fout.write("G21 ; set units to millimeters\n")
Fout.write("G90 ; use absolute coordinates\n")
Fout.write("M82 ; use absolute distances for extrusion\n")

for ii in range (2 , filelist.amount-1):
    # lay down insulating layer
    write_solidlayer(Fout);
    # read first Gerber layer
    metal_layer = read_Gerber(filelist[ii])
    union_boundary()
    contour_boundary()
    raster()
    #Lay down the metal 
    write_conduction(Fout)
    # Fill with insulator
    write_interlayer(Fout)
    # finish up close files
exit
        
     
    
