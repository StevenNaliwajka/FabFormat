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

    def __init__(self, config_file: string, infile, xoff,
                 yoff, size, outfile, undercut):
        self.infile = infile
        self.xoff = xoff
        self.yoff = yoff
        self.size = size
        self.outfile = outfile
        self.undercut = undercut
        config = self.read_config(config_file)
        for key, value in config:
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
