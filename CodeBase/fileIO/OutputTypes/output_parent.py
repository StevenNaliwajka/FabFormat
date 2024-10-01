from math import *
from CodeBase.misc.gui import Gui
from CodeBase.fileIO.universal_parent import UniversalParent
from CodeBase.misc.config import Config


# Contains Universal Methods for converting files.

class OutputParent(UniversalParent):
    def __init__(self):
        super().__init__()
        # hack: std dev of numerical noise to add to remove degeneracies
        self.NOISE = 1e-6
        # boundary is gotten from parsing input file and used in plot method
        self.boundary = []
        # boundary gets converted to toolpath and then fed into write OUTPUT files.
        self.toolpath = []
        # used in tandem with toolpath for plotting
        self.segplot = []

        # Only used in write files? strange...
        # results from ExcellionDrill files, holes.
        self.vias = []

        self.HUGE = 1e10
        # Used for the min/max pos of the board
        self.xmin = self.HUGE
        self.xmax = -self.HUGE
        self.ymin = self.HUGE
        self.ymax = -self.HUGE

        # No clue what this does...
        self.INTERSECT = 2

        # No clue what this does...
        self.SEG = 0
        # No clue what this does...
        self.VERT = 1

        # No clue what this does...
        self.A = 1

    def write_gui(self, input_file_obj_list, CONFIG:Config):
        # IMPLEMENTED by the write_xxxx.py file
        # Called IF CONFIG.gui_state == true
        pass

    def write_headless(self, input_file_obj_list, GUI: Gui):
        # IMPLEMENTED by the write_xxxx.py file
        # Called if CONFIG.gui_state != true
        pass

    def intersect(self, path, seg0, vert0, sega, verta):
        #
        # test and return edge intersection
        #
        if ((seg0 == sega) & (vert0 == 0) & (verta == (len(path[sega]) - 2))):
            # print ("    return (0-end)"
            return [[], []]
        x0 = path[seg0][vert0][self.X]
        y0 = path[seg0][vert0][self.Y]
        x1 = path[seg0][vert0 + 1][self.X]
        y1 = path[seg0][vert0 + 1][self.Y]
        dx01 = x1 - x0
        dy01 = y1 - y0
        d01 = sqrt(dx01 * dx01 + dy01 * dy01)
        if (d01 == 0):
            #
            # zero-length segment, return no intersection
            #
            # print ("zero-length segment"
            return [[], []]
        dxpar01 = dx01 / d01
        dypar01 = dy01 / d01
        dxperp01 = dypar01
        dyperp01 = -dxpar01
        xa = path[sega][verta][self.X]
        ya = path[sega][verta][self.Y]
        xb = path[sega][verta + 1][self.X]
        yb = path[sega][verta + 1][self.Y]
        dx0a = xa - x0
        dy0a = ya - y0
        dpar0a = dx0a * dxpar01 + dy0a * dypar01
        dperp0a = dx0a * dxperp01 + dy0a * dyperp01
        dx0b = xb - x0
        dy0b = yb - y0
        dpar0b = dx0b * dxpar01 + dy0b * dypar01
        dperp0b = dx0b * dxperp01 + dy0b * dyperp01
        # if (dperp0a*dperp0b >  self.EPS):
        if (((dperp0a > self.EPS) & (dperp0b > self.EPS)) | ((dperp0a < - self.EPS) & (dperp0b < - self.EPS))):
            #
            # vertices on same side, return no intersection
            #
            # print (" same side"
            return [[], []]
        elif ((abs(dperp0a) < self.EPS) & (abs(dperp0b) < self.EPS)):
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
        if ((d < - self.EPS) | (d > (d01 + self.EPS))):
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

    def union(self, i, path, intersections, sign):
        #
        # return edge to exit intersection i for a union
        #
        # print ("union: intersection",i,"in",intersections
        seg0 = intersections[i][0][self.SEG]
        # print ("seg0",seg0
        vert0 = intersections[i][0][self.VERT]
        x0 = path[seg0][vert0][self.X]
        y0 = path[seg0][vert0][self.Y]
        if (vert0 < (len(path[seg0]) - 1)):
            vert1 = vert0 + 1
        else:
            vert1 = 0
        x1 = path[seg0][vert1][self.X]
        y1 = path[seg0][vert1][self.Y]
        dx01 = x1 - x0
        dy01 = y1 - y0
        sega = intersections[i][self.A][self.SEG]
        verta = intersections[i][self.A][self.VERT]
        xa = path[sega][verta][self.X]
        ya = path[sega][verta][self.Y]
        if (verta < (len(path[sega]) - 1)):
            vertb = verta + 1
        else:
            vertb = 0
        xb = path[sega][vertb][self.X]
        yb = path[sega][vertb][self.Y]
        dxab = xb - xa
        dyab = yb - ya
        dot = dxab * dy01 - dyab * dx01
        # print ("    dot",dot)
        if (abs(dot) <= self.EPS):
            print("  colinear")
            seg = []
            vert = []
        elif (dot > self.EPS):
            seg = intersections[i][int((1 - sign) / 2)][self.SEG]
            vert = intersections[i][int((1 - sign) / 2)][self.VERT]
        else:
            seg = intersections[i][int((1 + sign) / 2)][self.SEG]
            vert = intersections[i][int((1 + sign) / 2)][self.VERT]
        return [seg, vert]

    def insert(self, path, x, y, seg, vert, intersection):
        #
        # insert a vertex at x,y in seg,vert, if needed
        #
        d0 = (path[seg][vert][self.X] - x) ** 2 + (path[seg][vert][self.Y] - y) ** 2
        d1 = (path[seg][vert + 1][self.X] - x) ** 2 + (path[seg][vert + 1][self.Y] - y) ** 2
        # print ("check insert seg",seg,"vert",vert,"intersection",intersection
        if ((d0 > self.EPS) & (d1 > self.EPS)):
            # print ("    added intersection vertex",vert+1
            path[seg].insert((vert + 1), [x, y, intersection])
            return 1
        elif (d0 < self.EPS):
            if (path[seg][vert][self.INTERSECT] == []):
                path[seg][vert][self.INTERSECT] = intersection
                # print ("    added d0",vert
            return 0
        elif (d1 < self.EPS):
            if (path[seg][vert + 1][self.INTERSECT] == []):
                path[seg][vert + 1][self.INTERSECT] = intersection
                # print ("    added d1",vert+1
            return 0
        else:
            # print ("    shouldn't happen: d0",d0,"d1",d1
            return 0

    def add_intersections(self, path, GUI: Gui):
        #
        # add vertices at path intersections
        #
        # global status, outframe, namedate
        intersection = 0
        #
        # loop over first edge
        #
        for seg0 in range(len(path)):
            GUI.status.set("    segment " + str(seg0) + "/" + str(len(path) - 1) + "  ")
            GUI.outframe.update()
            vert0 = 0
            N0 = len(path[seg0]) - 1
            while (vert0 < N0):
                #
                # loop over second edge
                #
                vert1 = vert0 + 2
                while (vert1 < N0):
                    #
                    # check for path self-intersection
                    #
                    [xloc, yloc] = self.intersect(path, seg0, vert0, seg0, vert1)
                    if (xloc != []):
                        #
                        # found intersection, insert vertices
                        #
                        n0 = self.insert(path, xloc, yloc, seg0, vert0, intersection)
                        N0 += n0
                        vert1 += n0
                        n1 = self.insert(path, xloc, yloc, seg0, vert1, intersection)
                        N0 += n1
                        vert1 += n1
                        if ((n0 > 0) | (n1 > 0)):
                            intersection += 1
                    vert1 += 1
                for sega in range((seg0 + 1), len(path)):
                    #
                    # check for intersection with other parts
                    #
                    # outframe.update()
                    verta = 0
                    Na = len(path[sega]) - 1
                    while (verta < Na):
                        [xloc, yloc] = self.intersect(path, seg0, vert0, sega, verta)
                        if (xloc != []):
                            #
                            # found intersection, insert vertices
                            #
                            n0 = self.insert(path, xloc, yloc, seg0, vert0, intersection)
                            N0 += n0
                            vert1 += n0
                            na = self.insert(path, xloc, yloc, sega, verta, intersection)
                            Na += na
                            verta += na
                            if ((n0 > 0) | (na > 0)):
                                intersection += 1
                        verta += 1
                vert0 += 1
        #
        # make vertex table and segment list of intersections
        #
        GUI.status.set(GUI.namedate)
        GUI.outframe.update()
        intersections = []
        for i in range(intersection):
            intersections.append([])
        for seg in range(len(path)):
            for vert in range(len(path[seg])):
                inters = path[seg][vert][self.INTERSECT]
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
                seg_intersections[intersections[i][0][self.SEG]].append(i)
                seg_intersections[intersections[i][self.A][self.SEG]].append(i)
        return [path, intersections, seg_intersections]

    def offset(self, x0, x1, x2, y0, y1, y2, r):
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
        if ((abs(dx0perp * dy1perp - dx1perp * dy0perp) < self.EPS) |
                (abs(dy0perp * dx1perp - dy1perp * dx0perp) < self.EPS)):
            dx = r * dx1perp
            dy = r * dy1perp
            # print ("    offset planar:",dx,dy
        elif ((abs(dx0perp + dx1perp) < self.EPS) & (abs(dy0perp + dy1perp) < self.EPS)):
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

    def displace(self, path, GUI: Gui):
        #
        # displace path inwards by tool radius if negitive
        #
        # global sundercut, sdia
        newpath = []
        scale = float(GUI.sscale.get())
        undercut = float(GUI.sundercut.get())
        toolrad = (float(GUI.sdia.get()) / 2.0 - undercut) / scale
        for seg in range(len(path)):
            newpath.append([])
            if (len(path[seg]) > 2):
                for vert1 in range(len(path[seg]) - 1):
                    if (vert1 == 0):
                        vert0 = len(path[seg]) - 2
                    else:
                        vert0 = vert1 - 1
                    vert2 = vert1 + 1
                    x0 = path[seg][vert0][self.X]
                    x1 = path[seg][vert1][self.X]
                    x2 = path[seg][vert2][self.X]
                    y0 = path[seg][vert0][self.Y]
                    y1 = path[seg][vert1][self.Y]
                    y2 = path[seg][vert2][self.Y]
                    [dx, dy] = self.offset(x0, x1, x2, y0, y1, y2, toolrad)
                    if (dx != []):
                        newpath[seg].append([(x1 + dx), (y1 + dy), []])
                        if (vert1 == 0):
                            xo = x1 + dx
                            yo = y1 + dy
                        x0 = newpath[seg][0][self.X]
                        y0 = newpath[seg][0][self.Y]
                    elif (len(path[seg]) == 2):
                        x0 = path[seg][0][self.X]
                        y0 = path[seg][0][self.Y]
                        x1 = path[seg][1][self.X]
                        y1 = path[seg][1][self.Y]
                        x2 = 2 * x1 - x0
                        y2 = 2 * y1 - y0
                        [dx, dy] = self.offset(x0, x1, x2, y0, y1, y2, toolrad)
                newpath[seg].append([xo, yo, []])
                x0 = newpath[seg][0][self.X]
                y0 = newpath[seg][0][self.Y]
                newpath[seg].append([x0, y0, []])
            else:
                print("  displace: shouldn't happen")
        return newpath

    def ccw(self, A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    def intersect1(self, A, B, C, D):
        return (self.ccw(A, C, D) != self.ccw(B, C, D)) and (self.ccw(A, B, C) != self.ccw(A, B, D))

    def point_in_polygon(self, pt, poly, inf):
        result = False
        for i in range(len(poly) - 1):
            if self.intersect1(poly[i], poly[i + 1], pt, [inf, pt[1]]):
                result = not result
        if self.intersect1(poly[-1], poly[0], pt, (inf, pt[1])):
            result = not result
        return result

    def in_me(self, x, y, poly):

        n = len(poly)
        inside = False

        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if ((p1x == p2x) or (x <= xints)):
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def print_intersections(self, path, intersections, seg):
        print("    Seg:" + str(seg) + " Intersections found:")
        for ii in range(len(path[seg]) - 1):
            intersect = path[seg][ii][self.INTERSECT]
            if (intersect != []):
                if (intersections[intersect] == []):
                    print("     " + str(intersect) + " Erased")
                else:
                    [seg0, vert0] = intersections[intersect][0]
                    [seg1, vert1] = intersections[intersect][1]
                    print(
                        "     " + str(intersect) + " = [" + str(seg0) + "," + str(vert0) + "][" + str(seg1) + "," + str(
                            vert1) + "],")
        return

    def new_prune(self, path, sign, event, GUI: Gui):
        #
        # new_prune path intersections
        #
        # first find the intersections
        #
        # global segplot
        print("    intersecting ...")
        # plot_path(event)
        # raw_input('before intersection')
        [path, intersections, seg_intersections] = self.add_intersections(path)
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
            if (self.point_in_polygon(point, poly, self.HUGE)):
                intersections[ii] = []
                print("     Intersection " + str(ii) + "inside poly")
            else:
                point = path[seg1][vert1]
                poly = path[seg0]
                if (self.point_in_polygon(point, poly, self.HUGE)):
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
            seg = intersections[i][0][self.SEG]
            vert = intersections[i][0][self.VERT]
            seg0 = seg
            vert0 = vert
            sega = intersections[i][1][self.SEG]  # ending segment and vertex
            verta = intersections[i][1][self.VERT]  # ending segment and vertex
            self.segplot = []
            self.segplot.append(path[seg])
            self.segplot.append(path[sega])
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
            forward = not self.point_in_polygon(point, poly, self.HUGE)
            print("     Go forward? " + str(forward))
            newseg = len(newpath)
            newpath.append([])
            x = path[seg][vert][self.X]
            y = path[seg][vert][self.Y]
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
                intersectindex = path[seg][vert][self.INTERSECT]
                if (intersectindex == []):
                    x = path[seg][vert][self.X]
                    y = path[seg][vert][self.Y]
                    newpath[newseg].append([])
                    newpath[newseg][vertc] = [x, y, []]
                    vertc += 1
                elif (intersectindex == i):
                    # we've come full circle
                    x = path[seg0][vert0][self.X]
                    y = path[seg0][vert0][self.Y]
                    newpath[newseg].append([])
                    newpath[newseg][vertc] = [x, y, []]
                    print("Segment complete [" + str(seg0) + "," + str(vert0) + "] \n\n")
                    break
                else:
                    x = path[seg][vert][self.X]
                    y = path[seg][vert][self.Y]
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
                        self.segplot.append(path[sega])
                        self.plot_seg(event)
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
                        forward = not self.point_in_polygon(point, poly, self.HUGE)
                        print("     Go forward? " + str(forward))
                        print("      new vertex = " + str(vert))
                    # end if
                # end if
            # end while
        return newpath

    def prune(self, path, sign, event):
        #
        # prune path intersections
        #
        # first find the intersections
        #
        print("    intersecting ...")
        # plot_path(event)
        # raw_input('before intersection')
        [path, intersections, seg_intersections] = self.add_intersections(path)
        # print 'path:',path
        # print 'intersections:',intersections
        # print 'seg_intersections:',seg_intersections
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
        # finally follow and remove the intersections
        #
        print("    pruning ...")
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
                interior = 1
                while 1:
                    # print 'testing intersection',intersection,':',intersections[intersection]
                    if (intersections[intersection] == []):
                        seg = oldseg
                    else:
                        [seg, vert] = self.union(intersection, path, intersections, sign)
                        # print '  seg',seg,'vert',vert,'oldseg',oldseg
                    if (seg == oldseg):
                        # print ("    remove interior intersection",istart
                        seg0 = intersections[istart][0][self.SEG]
                        vert0 = intersections[istart][0][self.VERT]
                        path[seg0][vert0][self.INTERSECT] = -1
                        seg1 = intersections[istart][1][self.SEG]
                        vert1 = intersections[istart][1][self.VERT]
                        path[seg1][vert1][self.INTERSECT] = -1
                        intersections[istart] = []
                        break
                    elif (seg == []):
                        seg = intersections[intersection][0][self.SEG]
                        vert = intersections[intersection][0][self.SEG]
                        oldseg = []
                    else:
                        oldseg = seg
                        intersection = []
                        while (intersection == []):
                            if (vert < (len(path[seg]) - 1)):
                                vert += 1
                            else:
                                vert = 0
                            intersection = path[seg][vert][self.INTERSECT]
                        if (intersection == -1):
                            intersection = istart
                            break
                        elif (intersection == istart):
                            # print '    back to',istart
                            interior = 0
                            intersection = istart
                            break
                #
                # save path if valid boundary intersection
                #
                if (interior == 0):
                    newseg = len(newpath)
                    newpath.append([])
                    while 1:
                        # print 'keeping intersection',intersection,':',intersections[intersection]
                        [seg, vert] = self.union(intersection, path, intersections, sign)
                        if (seg == []):
                            seg = intersections[intersection][0][self.SEG]
                            vert = intersections[intersection][0][self.VERT]
                        # print '  seg',seg,'vert',vert
                        intersections[intersection] = []
                        intersection = []
                        while (intersection == []):
                            if (vert < (len(path[seg]) - 1)):
                                x = path[seg][vert][self.X]
                                y = path[seg][vert][self.Y]
                                newpath[newseg].append([x, y, []])
                                vert += 1
                            else:
                                vert = 0
                            intersection = path[seg][vert][self.INTERSECT]
                        if (intersection == istart):
                            # print '    back to',istart
                            x = path[seg][vert][self.X]
                            y = path[seg][vert][self.Y]
                            newpath[newseg].append([x, y, []])
                            break
                i += 1
        return newpath

    def union_boundary(self, event, GUI: Gui):
        # global boundary, intersections
        #
        # union intersecting polygons on boundary
        #
        print("union  self.boundary ...")
        sign = 1
        # boundary = prune(boundary,sign,event)
        self.boundary = self.new_prune(self.boundary, sign, event)
        print("    done")
        GUI.plot(event)

    def contour_boundary(self, event, GUI: Gui):
        # global boundary, toolpath
        #
        # contour boundary to find toolpath
        #
        print("contouring boundary ...")
        undercut = float(GUI.sundercut.get())
        if (undercut != 0.0):
            print("    undercutting contour by", undercut)
            #
            # displace vertices inward by tool size
            #
            print("    displacing ...")
            self.toolpath = self.displace(self.boundary)
        else:
            print("     WARNING: no displacement set")
        GUI.plot(event)
        print('displaced')
        sign = -1
        # self.toolpath = new_prune(self.toolpath,sign,event)
        GUI.plot(event)
        print("    done")

    def raster(self, event, GUI: Gui):
        # global boundary, toolpath, ymin, ymax
        #
        # raster interior
        #
        print("rastering interior ...")
        scale = float(GUI.sscale.get())
        tooldia = float(GUI.sdia.get()) / scale
        overlap = float(GUI.soverlap.get())
        if (self.toolpath == []):
            edgepath = self.boundary
            delta = tooldia / 2.0
        else:
            edgepath = self.toolpath
            delta = tooldia / 4.0
        #
        # find row-edge intersections
        #
        edges = []
        dymin = self.ymin - 2 * tooldia * overlap
        dymax = self.ymax + 2 * tooldia * overlap
        row1 = int(floor((dymax - dymin) / (tooldia * overlap)))
        for row in range(row1 + 1):
            edges.append([])
        for seg in range(len(edgepath)):
            for vertex in range(len(edgepath[seg]) - 1):
                x0 = edgepath[seg][vertex][self.X]
                y0 = edgepath[seg][vertex][self.Y]
                x1 = edgepath[seg][vertex + 1][self.X]
                y1 = edgepath[seg][vertex + 1][self.Y]
                if (y1 == y0):
                    continue
                elif (y1 < y0):
                    x0, x1 = x1, x0
                    y0, y1 = y1, y0
                row0 = int(ceil((y0 - dymin) / (tooldia * overlap)))
                row1 = int(floor((y1 - dymin) / (tooldia * overlap)))
                for row in range(row0, (row1 + 1)):
                    y = dymin + row * tooldia * overlap
                    x = x0 * (y1 - y) / (y1 - y0) + x1 * (y - y0) / (y1 - y0)
                    edges[row].append(x)
        for row in range(len(edges)):
            edges[row].sort()
            y = dymin + row * tooldia * overlap
            edge = 0
            while edge < len(edges[row]):
                x0 = edges[row][edge] + delta
                edge += 1
                if (edge < len(edges[row])):
                    x1 = edges[row][edge] - delta
                else:
                    print("shouldn't happen: row", row, "length", len(edges[row]))
                    break
                edge += 1
                if (x0 < x1):
                    self.toolpath.append([])
                    self.toolpath[-1].append([x0, y, []])
                    self.toolpath[-1].append([x1, y, []])
        GUI.plot(event)
        print("    done")
