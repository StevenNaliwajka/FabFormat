import os
import string
import tkinter as tk
from CodeBase.DataStructure.config_data import Config_Data
from datetime import date


class GUI_Data():
    # Config Data

    _inframe = None
    _root = None
    _GUIInfile = None
    _GUIOutfile = None
    _winfile = None
    _ssize = None
    _wsize = None
    _ivert = None
    _wvert = None

    _coordframe = None
    _sxoff = None
    _syoff = None
    _sscale = None
    _wxoff = None
    _wyoff = None
    _wscale = None

    _c = None

    _outframe = None
    _namedate = None
    _status = None
    _woutfile = None

    _camframe = None
    _unionbtn = None
    _contourbtn = None
    _rasterbtn = None
    _writebtn = None

    _toolframe = None
    _sdia = None
    _wtooldia = None
    _sundercut = None
    _soverlap = None
    _wundercut = None
    _wonderlap = None
    _wolverlap = None

    _millframe = None
    _szup = None
    _szdown = None
    _sxyvel = None
    _szvel = None

    _gframe = None
    _sztop = None
    _szbottom = None
    _sfeed = None
    _sspindle = None
    _stool = None

    _cutframe = None
    _sforce = None
    _svel = None

    _laserframe = None
    _srate = None
    _spower = None
    _sspeed = None

    _imgframe = None
    _sximg = None
    _syimg = None

    def __init__(self):
        self._root = tk.Tk()
        self.GUIinfile = tk.StringVar()
        self.GUIoutfile = tk.StringVar()
        self._ssize = tk.StringVar()
        self._ivert = tk.IntVar()
        self._sxoff = tk.StringVar()
        self._syoff = tk.StringVar()
        self._sscale = tk.StringVar()
        self._status = tk.StringVar()
        self._sdia = tk.StringVar()
        self._sundercut = tk.StringVar()
        self._soverlap = tk.StringVar()
        self._szup = tk.StringVar()
        self._szdown = tk.StringVar()
        self._sxyvel = tk.StringVar()
        self._szvel = tk.StringVar()
        self._sztop = tk.StringVar()
        self._szbottom = tk.StringVar()
        self._sfeed = tk.StringVar()
        self._sspindle = tk.StringVar()
        self._stool = tk.StringVar()
        self._sforce = tk.StringVar()
        self._svel = tk.StringVar()
        self._srate = tk.StringVar()
        self._spower = tk.StringVar()
        self._sspeed = tk.StringVar()
        self._sximg = tk.StringVar()
        self._syimg = tk.StringVar()

    # GETTERS
    @property
    def root(self):
        return self._root

    @property
    def guiinfile(self):
        return self._GUIInfile

    @property
    def guioutfile(self):
        return self._GUIOutfile

    @property
    def winfile(self):
        return self._winfile

    @property
    def ssize(self):
        return self._ssize

    @property
    def wsize(self):
        return self._wsize

    @property
    def ivert(self):
        return self._ivert

    @property
    def wvert(self):
        return self._wvert

    @property
    def sxoff(self):
        return self._sxoff

    @property
    def syoff(self):
        return self._syoff

    @property
    def sscale(self):
        return self._sscale

    @property
    def wxoff(self):
        return self._wxoff

    @property
    def wyoff(self):
        return self._wyoff

    @property
    def wscale(self):
        return self._wscale

    @property
    def namedate(self):
        return self._namedate

    @property
    def status(self):
        return self._status

    @property
    def woutfile(self):
        return self._woutfile

    @property
    def unionbtn(self):
        return self._unionbtn

    @property
    def contourbtn(self):
        return self._contourbtn

    @property
    def rasterbtn(self):
        return self._rasterbtn

    @property
    def writebtn(self):
        return self._writebtn

    @property
    def sdia(self):
        return self._sdia

    @property
    def wtooldia(self):
        return self._wtooldia

    @property
    def sundercut(self):
        return self._sundercut

    @property
    def soverlap(self):
        return self._soverlap

    @property
    def wundercut(self):
        return self._wundercut

    @property
    def wonderlap(self):
        return self._wonderlap

    @property
    def wolverlap(self):
        return self._wolverlap

    @property
    def szup(self):
        return self._szup

    @property
    def szdown(self):
        return self._szdown

    @property
    def sxyvel(self):
        return self._sxyvel

    @property
    def szvel(self):
        return self._szvel

    @property
    def sztop(self):
        return self._sztop

    @property
    def szbottom(self):
        return self._szbottom

    @property
    def sfeed(self):
        return self._sfeed

    @property
    def sspindle(self):
        return self._sspindle

    @property
    def stool(self):
        return self._stool

    @property
    def sforce(self):
        return self._sforce

    @property
    def svel(self):
        return self._svel

    @property
    def srate(self):
        return self._srate

    @property
    def spower(self):
        return self._spower

    @property
    def sspeed(self):
        return self._sspeed

    @property
    def sximg(self):
        return self._sximg

    @property
    def syimg(self):
        return self._syimg

    @property
    def inframe(self):
        return self._inframe

    @property
    def coordframe(self):
        return self._coordframe

    @property
    def outframe(self):
        return self._outframe

    @property
    def camframe(self):
        return self._camframe

    @property
    def toolframe(self):
        return self._toolframe

    @property
    def millframe(self):
        return self._millframe

    @property
    def gframe(self):
        return self._gframe
    @property
    def cutframe(self):
        return self._cutframe

    @property
    def laserframe(self):
        return self._laserframe

    @property
    def imgframe(self):
        return self._imgframe

    @property
    def c(self):
        return self._c

    # SETTERS
    @root.setter
    def root(self, root):
        self._root = root

    @guiinfile.setter
    def guiinfile(self, GUIInfile):
        self._GUIInfile = GUIInfile

    @guioutfile.setter
    def guioutfile(self, GUIOutfile):
        self._GUIOutfile = GUIOutfile

    @winfile.setter
    def winfile(self, winfile):
        self._winfile = winfile

    @ssize.setter
    def ssize(self, ssize):
        self._ssize = ssize

    @wsize.setter
    def wsize(self, wsize):
        self._wsize = wsize

    @ivert.setter
    def ivert(self, ivert):
        self._ivert = ivert

    @wvert.setter
    def wvert(self, wvert):
        self._wvert = wvert

    @sxoff.setter
    def sxoff(self, sxoff):
        self._sxoff = sxoff

    @syoff.setter
    def syoff(self, syoff):
        self._syoff = syoff

    @sscale.setter
    def sscale(self, sscale):
        self._sscale = sscale

    @wxoff.setter
    def wxoff(self, wxoff):
        self._wxoff = wxoff

    @wyoff.setter
    def wyoff(self, wyoff):
        self._wyoff = wyoff

    @wscale.setter
    def wscale(self, wscale):
        self._wscale = wscale

    @namedate.setter
    def namedate(self, namedate):
        self._namedate = namedate

    @status.setter
    def status(self, status):
        self._status = status

    @woutfile.setter
    def woutfile(self, woutfile):
        self._woutfile = woutfile

    @unionbtn.setter
    def unionbtn(self, unionbtn):
        self._unionbtn = unionbtn

    @contourbtn.setter
    def contourbtn(self, contourbtn):
        self._contourbtn = contourbtn

    @rasterbtn.setter
    def rasterbtn(self, rasterbtn):
        self._rasterbtn = rasterbtn

    @writebtn.setter
    def writebtn(self, writebtn):
        self._writebtn = writebtn

    @sdia.setter
    def sdia(self, sdia):
        self._sdia = sdia

    @wtooldia.setter
    def wtooldia(self, wtooldia):
        self._wtooldia = wtooldia

    @sundercut.setter
    def sundercut(self, sundercut):
        self._sundercut = sundercut

    @soverlap.setter
    def soverlap(self, soverlap):
        self._soverlap = soverlap


    @wundercut.setter
    def wundercut(self, wundercut):
        self._wundercut = wundercut

    @wonderlap.setter
    def wonderlap(self, wonderlap):
        self._wonderlap = wonderlap

    @wolverlap.setter
    def wolverlap(self, woverlap):
        self._wolverlap = woverlap

    @szup.setter
    def szup(self, szup):
        self._szup = szup

    @szdown.setter
    def szdown(self, szdown):
        self._szdown = szdown

    @szdown.setter
    def sxyvel(self, sxyvel):
        self._sxyvel = sxyvel

    @szvel.setter
    def szvel(self, szvel):
        self._szvel = szvel

    @sztop.setter
    def sztop(self, sztop):
        self._sztop = sztop

    @szbottom.setter
    def szbottom(self, szbottom):
        self._szbottom = szbottom

    @sfeed.setter
    def sfeed(self, sfeed):
        self._sfeed = sfeed

    @sspindle.setter
    def sspindle(self, sspindle):
        self._sspindle = sspindle

    @stool.setter
    def stool(self, stool):
        self._stool = stool

    @sforce.setter
    def sforce(self, sforce):
        self._sforce = sforce

    @svel.setter
    def svel(self, svel):
        self._svel = svel

    @srate.setter
    def srate(self, srate):
        self._srate = srate

    @spower.setter
    def spower(self, spower):
        self._spower = spower

    @sspeed.setter
    def sspeed(self, sspeed):
        self._sspeed = sspeed

    @sximg.setter
    def sximg(self, sximg):
        self._sximg = sximg

    @syimg.setter
    def syimg(self, syimg):
        self._syimg = syimg

    @inframe.setter
    def inframe(self, inframe):
        self._inframe = inframe

    @coordframe.setter
    def coordframe(self, coordframe):
        self._coordframe = coordframe

    @outframe.setter
    def outframe(self, outframe):
        self._outframe = outframe

    @camframe.setter
    def camframe(self, camframe):
        self._camframe = camframe

    @toolframe.setter
    def toolframe(self, toolframe):
        self._toolframe = toolframe

    @millframe.setter
    def millframe(self, millframe):
        self._millframe = millframe

    @gframe.setter
    def gframe(self, gframe):
        self._gframe = gframe

    @cutframe.setter
    def cutframe(self, cutframe):
        self._cutframe = cutframe

    @laserframe.setter
    def laserframe(self, laserframe):
        self._laserframe = laserframe

    @imgframe.setter
    def imgframe(self, imgframe):
        self._imgframe = imgframe

    @c.setter
    def c(self,c):
        self._c = c