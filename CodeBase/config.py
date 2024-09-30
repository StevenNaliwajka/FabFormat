import os
import string
from datetime import date


class Config():
    # Config Data

    def __init__(self, infileDirectoryPath: string, outfileDirectoryPath: string):

        self._infileDirectoryPath = infileDirectoryPath
        self._outfileDirectoryPath = outfileDirectoryPath
        # Generates paths
        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)
        parent_dir = os.path.dirname(current_dir)

        # Generates path of GUI CONFIG
        gui_config_path = os.path.join(parent_dir, "gui_config.txt")

        # Generates path of INFILE CONFIG
        infile_config_path = os.path.join(infileDirectoryPath, "config.txt")

        # Reads in GUI CONFIG
        self.update_config_handler(self.read_gui_config(gui_config_path), gui_config_path)
        # Reads in INPUT CONFIG
        self.update_config_handler(self.read_input_config(infile_config_path), infile_config_path)

        self._date = date.today()

        self.scale = 1.0
        self.gscale = 25.4  # assuming gerber is in inches and scad must be in mm
        self.sthickness = 0.1  # substrate thickness
        self.mthickness = 0.0075  # metal thickness in inches 0.19mm
        self.mwidth = 0.01  # conductor width in inces 0.25mm
        self.size = 2.0
        self.xoff = 0.1
        self.yoff = 0.1

        self.infile = None
        self.list = None
        self.outfile = None
        self.type = None
        self.infile = None
        self.file = None
        self.location = None
        self.outifle = None
        self.folder = None

    def read_gui_config(self, gui_config_path):
        # Reads GUI CONFIG file and passes back a parsed array
        config = {}
        with open(gui_config_path, 'r') as file:
            content = file.read()
            lines = content.splitlines()
            for line in lines:
                # ignore comments + blank lines
                if line.strip() and not line.startswith("#") and not line == "":
                    # Parse it and add it to config array to send back
                    key, value = line.strip().split("=")
                    config[key.strip()] = value.strip()
        file.close()
        return config

    def read_input_config(self, input_config_path):
        # Reads INPUT CONFIG and passes back a parsed array
        config = {}
        with open(input_config_path, 'r') as file:
            content = file.read()
            lines = content.splitlines()
            for line in lines:
                # ignore comments + blank lines
                if line.strip() and not line.startswith("#") and not line == "":
                    # Parse it and add it to config dict to send back
                    if line.startswith("-"):
                        # If a file, indicated with a "-" prefix, add to the file list
                        self._inputFileList.append(line[1:].strip())
                    else:
                        # If else, update main config
                        key, value = line.strip().split("=")
                        config[key.strip()] = value.strip()
        file.close()
        return config

    def update_config_handler(self, parsed_config_file, config_path: string):
        # Reads parsed array and updates the main config object.
        for key, value in parsed_config_file.items():
            if hasattr(self, key):
                try:
                    setattr(self, key, value)
                    #print(f"{key} successfully set to {value}")
                except AttributeError as e:
                    print(f"CONFIG_Data: Error setting {key}: {e}")
            else:
                print(f"Config Handler: {config_path} is built incorrectly, {key} is incorrectly configured.")

    # GETTERS --------------------------
    @property
    def window(self):
        return self._window

    @property
    def eps(self):
        return self._eps

    @property
    def noise(self):
        return self._noise

    @property
    def scale(self):
        return self._scale

    @property
    def gscale(self):
        return self._gscale

    @property
    def sthickness(self):
        return self._sthickness

    @property
    def mthickness(self):
        return self._mthickness

    @property
    def mwidth(self):
        return self._mwidth

    @property
    def boardsize(self):
        return self._boardsize

    @property
    def boardxoff(self):
        return self._boardxoff

    @property
    def boardyoff(self):
        return self._boardyoff

    @property
    def xmin(self):
        return self._xmin

    @property
    def xmax(self):
        return self._xmax

    @property
    def ymin(self):
        return self._ymin

    @property
    def ymax(self):
        return self._ymax

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def HUGE(self):
        return self._HUGE

    @property
    def INTERSECT(self):
        return self._INTERSECT

    @property
    def SEG(self):
        return self._SEG

    @property
    def VERT(self):
        return self._VERT

    @property
    def A(self):
        return self._A

    @property
    def TYPE(self):
        return self._TYPE

    @property
    def WIDTH(self):
        return self._WIDTH

    @property
    def HEIGHT(self):
        return self._HEIGHT

    @property
    def NVERTS(self):
        return self._NVERTS

    @property
    def TRUEVALUE(self):
        return self._TRUEVALUE

    @property
    def FALSEVALUE(self):
        return self._FALSEVALUE

    @property
    def infilename(self):
        return self._infilename

    @property
    def outfilename(self):
        return self._outfilename

    @property
    def undercut(self):
        return self._undercut

    @property
    def boundary(self):
        return self._boundary

    @property
    def toolpath(self):
        return self._toolpath

    @property
    def itoolpath(self):
        return self._itoolpath
    @property
    def segplot(self):
        return self._segplot

    @property
    def vias(self):
        return self._vias

    @property
    def infileDirectoryPath(self):
        return self._infileDirectoryPath

    @property
    def outfileDirectoryPath(self):
        return self._outfileDirectoryPath

    @property
    def inputFileList(self):
        return self._inputFileList

    @property
    def outputType(self):
        return self._outputType

    @property
    def date(self):
        return self._date

    # SETTERS --------------------------
    @window.setter
    def window(self, window):
        self._window = window

    @eps.setter
    def eps(self, eps):
        self._eps = eps

    @noise.setter
    def noise(self, noise):
        self._noise = noise

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @gscale.setter
    def gscale(self, gscale):
        self._gscale = gscale

    @sthickness.setter
    def sthickness(self, sthickness):
        self._sthickness = sthickness

    @mthickness.setter
    def mthickness(self, mthickness):
        self.mthicknes = mthickness

    @mwidth.setter
    def mwidth(self, mwidth):
        self._mwidth = mwidth

    @boardsize.setter
    def size(self, size):
        self._boardsize = size

    @boardxoff.setter
    def xoff(self, xoff):
        self._boardxoff = xoff

    @boardyoff.setter
    def yoff(self, yoff):
        self._boardyoff = yoff

    @xmin.setter
    def xmin(self, xmin):
        self._xmin = xmin

    @xmax.setter
    def xmax(self, xmax):
        self._xmax = xmax

    @ymin.setter
    def ymin(self, ymin):
        self._ymin = ymin

    @ymax.setter
    def ymax(self, ymax):
        self._ymax = ymax

    @X.setter
    def X(self, X):
        self._X = X

    @Y.setter
    def Y(self, Y):
        self._Y = Y

    @INTERSECT.setter
    def INTERSECT(self, INTERSECT):
        self._INTERSECT = INTERSECT

    @SEG.setter
    def SEG(self, SEG):
        self._SEG = SEG

    @VERT.setter
    def VERT(self, VERT):
        self._VERT = VERT

    @A.setter
    def A(self, A):
        self._A = A

    @TYPE.setter
    def TYPE(self, TYPE):
        self._TYPE = TYPE

    @WIDTH.setter
    def WIDTH(self, WIDTH):
        self._WIDTH = WIDTH

    @HEIGHT.setter
    def HEIGHT(self, HEIGHT):
        self._HEIGHT = HEIGHT

    @outputType.setter
    def outputType(self, outputType):
        self._outputType = outputType

    @NVERTS.setter
    def NVERTS(self, NVERTS):
        self._NVERTS = NVERTS

    @TRUEVALUE.setter
    def TRUEVALUE(self, TRUEVALUE):
        self._TRUEVALUE = TRUEVALUE

    @FALSEVALUE.setter
    def FALSEVALUE(self, FALSEVALUE):
        self._FALSEVALUE = FALSEVALUE

    @infilename.setter
    def infilename(self, infilename):
        self._infilename = infilename

    @outfilename.setter
    def outfilename(self, outfilename):
        self._outfilename = outfilename

    @undercut.setter
    def undercut(self, undercut):
        self._undercut = undercut

    @boundary.setter
    def boundary(self, boundary):
        self._boundary = boundary

    @toolpath.setter
    def toolpath(self, toolpath):
        self._toolpath = toolpath

    @itoolpath.setter
    def itoolpath(self, itoolpath):
        self._itoolpath = itoolpath

    @segplot.setter
    def segplot(self, segplot):
        self._segplot = segplot

    @vias.setter
    def vias(self, vias):
        self._vias = vias

