import os
import string
from datetime import date


class Config_Handler():
    # Config Data
    infileDirectoryPath = None
    outfileDirectoryPath = None
    inputFileList = []
    outputType = None
    window = None
    eps = None
    noise = None
    scale = None
    gscale = None
    sthickness = None
    mthickness = None
    mwidth = None
    xmin = None
    xmax = None
    ymin = None
    ymax = None
    X = None
    Y = None
    INTERSECT = None
    SEG = None
    VERT = None
    A = None
    TYPE = None
    # NOTE SIZE and size are both included. Not sure the diff... TBD
    SIZE = None
    WIDTH = None
    HEIGHT = None
    NVERTS = None
    TRUE = None
    FALSE = None

    infile = None
    xoff = None
    yoff = None
    size = None
    outfile = None
    undercut = None
    boundary = None
    toolpath = None
    itoolpath = None
    infile = None
    segplot = None
    vias = None
    date = None

    def __init__(self, infileDirectoryPath: string, outfileDirectoryPath: string):

        self.infileDirectoryPath = infileDirectoryPath
        self.outfileDirectoryPath = outfileDirectoryPath
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

        self.date = date.today()

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
                        self.inputFileList.append(line[1:].strip())
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
                setattr(self, key, value)
            else:
                print(f"Config Handler: {config_path} is built incorrectly, {key} is incorrectly configured.")

    # GETTERS --------------------------
    def get_window(self):
        return self.window

    def get_eps(self):
        return self.eps

    def get_noise(self):
        return self.noise

    def get_scale(self):
        return self.scale

    def get_gscale(self):
        return self.gscale

    def get_sthickness(self):
        return self.sthickness

    def get_mthickness(self):
        return self.mthickness

    def get_mwidth(self):
        return self.mwidth

    def get_size(self):
        return self.size

    def get_xoff(self):
        return self.xoff

    def get_yoff(self):
        return self.yoff

    def get_xmin(self):
        return self.xmin

    def get_xmax(self):
        return self.xmax

    def get_ymin(self):
        return self.ymin

    def get_ymax(self):
        return self.ymax

    def get_X(self):
        return self.X

    def get_Y(self):
        return self.Y

    def get_INTERSECT(self):
        return self.INTERSECT

    def get_SEG(self):
        return self.SEG

    def get_VERT(self):
        return self.VERT

    def get_A(self):
        return self.A

    def get_TYPE(self):
        return self.TYPE

    def get_WIDTH(self):
        return self.WIDTH

    def get_HEIGHT(self):
        return self.HEIGHT

    def get_NVERTS(self):
        return self.NVERTS

    def get_TRUE(self):
        return self.TRUE

    def get_FALSE(self):
        return self.FALSE

    def get_infile(self):
        return self.infile

    def get_xoff(self):
        return self.xoff

    def get_yoff(self):
        return self.yoff

    def get_size(self):
        return self.size

    def get_outfile(self):
        return self.outfile

    def get_undercut(self):
        return self.undercut

    def get_boundary(self):
        return self.boundary

    def get_toolpath(self):
        return self.toolpath

    def get_itoolpath(self):
        return self.itoolpath

    def get_infile(self):
        return self.infile

    def get_segplot(self):
        return self.segplot

    def get_vias(self):
        return self.vias

    def get_infileDirectoryPath(self):
        return self.infileDirectoryPath

    def get_outfileDirectoryPath(self):
        return self.outfileDirectoryPath

    def get_inputFileList(self):
        return self.inputFileList

    def get_outputType(self):
        return self.outputType

    def get_date(self):
        return self.date

    # SETTERS --------------------------
    def set_window(self, window):
        self.window = window

    def set_eps(self, eps):
        self.eps = eps

    def set_noise(self, noise):
        self.noise = noise

    def set_scale(self, scale):
        self.scale = scale

    def set_gscale(self, gscale):
        self.gscale = gscale

    def set_sthickness(self, sthickness):
        self.sthickness = sthickness

    def set_mthickness(self, mthickness):
        self.mthicknes = mthickness

    def set_mwidth(self, mwidth):
        self.mwidth = mwidth

    def set_size(self, size):
        self.size = size

    def set_xoff(self, xoff):
        self.xoff = xoff

    def set_yoff(self, yoff):
        self.yoff = yoff

    def set_xmin(self, xmin):
        self.xmin = xmin

    def set_xmax(self, xmax):
        self.xmax = xmax

    def set_ymin(self, ymin):
        self.ymin = ymin

    def set_ymax(self, ymax):
        self.ymax = ymax

    def set_X(self, X):
        self.X = X

    def set_Y(self, Y):
        self.Y = Y

    def set_INTERSECT(self, INTERSECT):
        self.INTERSECT = INTERSECT

    def set_SEG(self, SEG):
        self.SEG = SEG

    def set_VERT(self, VERT):
        self.VERT = VERT

    def set_A(self, A):
        self.A = A

    def set_TYPE(self, TYPE):
        self.TYPE = TYPE

    def set_WIDTH(self, WIDTH):
        self.WIDTH = WIDTH

    def set_HEIGHT(self, HEIGHT):
        self.HEIGHT  =HEIGHT

    def set_NVERTS(self, NVERTS):
        self.NVERTS = NVERTS

    def set_TRUE(self, TRUE):
        self.TRUE = TRUE

    def set_FALSE(self, FALSE):
        self.FALSE = FALSE

    def set_infile(self, infile):
        self.infile = infile

    def set_xoff(self, xoff):
        self.xoff = xoff

    def set_yoff(self, yoff):
        self.yoff = yoff

    def set_size(self, size):
        self.size = size

    def set_outfile(self, outfile):
        self.outfile = outfile

    def set_undercut(self, undercut):
        self.undercut = undercut

    def set_boundary(self, boundary):
        self.boundary = boundary

    def set_toolpath(self, toolpath):
        self.toolpath = toolpath

    def set_itoolpath(self, itoolpath):
        self.itoolpath = itoolpath

    def set_infile(self, infile):
        self.infile = infile

    def set_segplot(self, segplot):
        self.segplot = segplot

    def set_vias(self, vias):
        self.vias = vias

