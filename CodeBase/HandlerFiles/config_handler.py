import os
import string


class Config_Handler():
    # Config Data
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

    def __init__(self, config_file: string, infile, xoff,
                 yoff, size, outfile, undercut):

        self.infile = infile
        self.xoff = xoff
        self.yoff = yoff
        self.size = size
        self.outfile = outfile
        self.undercut = undercut

        # Generates the path of the config file.
        # config file must be in CodeBase folder.
        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)
        parent_dir = os.path.dirname(current_dir)
        config_file_location = os.path.join(parent_dir, config_file)


        config = self.read_config(config_file_location)
        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Config Handler: {config_file} is built incorrectly, {key} is incorrectly configured.")

    def read_config(self, file_path):
        config = {}
        with open(file_path, 'r') as file:
            for line in file:
                # ignore comments + blank lines
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=")
                    config[key.strip()] = value.strip()
        return config

    # GETTERS --------------------------
    def get_window(self): return self.window
    def get_eps(self): return self.eps
    def get_noise(self): return self.noise
    def get_scale(self): return self.scale
    def get_gscale(self): return self.gscale
    def get_sthickness(self): return self.sthickness
    def get_mthickness(self): return self.mthickness
    def get_mwidth(self): return self.mwidth
    def get_size(self): return self.size
    def get_xoff(self): return self.xoff
    def get_yoff(self): return self.yoff
    def get_xmin(self): return self.xmin
    def get_xmax(self): return self.xmax
    def get_ymin(self): return self.ymin
    def get_ymax(self): return self.ymax
    def get_X(self): return self.X
    def get_Y(self): return self.Y
    def get_INTERSECT(self): return self.INTERSECT
    def get_SEG(self): return self.SEG
    def get_VERT(self): return self.VERT
    def get_A(self): return self.A
    def get_TYPE(self): return self.TYPE
    def get_WIDTH(self): return self.WIDTH
    def get_HEIGHT(self): return self.HEIGHT
    def get_NVERTS(self): return self.NVERTS
    def get_TRUE(self): return self.TRUE
    def get_FALSE(self): return self.FALSE
    def get_infile(self): return self.infile
    def get_xoff(self): return self.xoff
    def get_yoff(self): return self.yoff
    def get_size(self): return self.size
    def get_outfile(self): return self.outfile
    def get_undercut(self): return self.undercut
    def get_boundary(self): return self.boundary
    def get_toolpath(self): return self.toolpath
    def get_itoolpath(self): return self.itoolpath
    def get_infile(self): return self.infile
    def get_segplot(self): return self.segplot
    def get_vias(self): return self.vias

    # SETTERS --------------------------
    def set_window(self, window): self.window = window
    def set_eps(self, eps): self.eps = eps
    def set_noise(self, noise): self.noise = noise
    def set_scale(self, scale): self.scale = scale
    def set_gscale(self, gscale): self.gscale = gscale
    def set_sthickness(self, sthickness): self.sthickness = sthickness
    def set_mthickness(self, mthickness): self.mthicknes = mthickness
    def set_mwidth(self, mwidth): self.mwidth = mwidth
    def set_size(self, size): self.size = size
    def set_xoff(self, xoff): self.xoff = xoff
    def set_yoff(self, yoff): self.yoff = yoff
    def set_xmin(self, xmin): self.xmin = xmin
    def set_xmax(self, xmax): self.xmax = xmax
    def set_ymin(self, ymin): self.ymin = ymin
    def set_ymax(self, ymax): self.ymax = ymax
    def set_X(self, X): self.X = X
    def set_Y(self, Y): self.Y = Y
    def set_INTERSECT(self, INTERSECT): self.INTERSECT = INTERSECT
    def set_SEG(self, SEG): self.SEG = SEG
    def set_VERT(self, VERT): self.VERT = VERT
    def set_A(self, A): self.A = A
    def set_TYPE(self, TYPE): self.TYPE
    def set_WIDTH(self, WIDTH): self.WIDTH
    def set_HEIGHT(self, HEIGHT): self.HEIGHT
    def set_NVERTS(self, NVERTS): self.NVERTS
    def set_TRUE(self, TRUE): self.TRUE
    def set_FALSE(self, FALSE): self.FALSE
    def set_infile(self, infile): self.infile
    def set_xoff(self, xoff): self.xoff
    def set_yoff(self, yoff): self.yoff
    def set_size(self, size): self.size
    def set_outfile(self, outfile): self.outfile
    def set_undercut(self, undercut): self.undercut
    def set_boundary(self, boundary): self.boundary
    def set_toolpath(self, toolpath): self.toolpath
    def set_itoolpath(self, itoolpath): self.itoolpath
    def set_infile(self, infile): self.infile
    def set_segplot(self, segplot): self.segplot
    def set_vias(self, vias): self.vias