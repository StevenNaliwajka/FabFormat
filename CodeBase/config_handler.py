import string


class Config_Handler():
    window = None
    eps = None
    noise = None
    scale = None
    gscale = None
    sthickness = None
    mthickness = None
    mwidth = None
    size = None
    xoff = None
    yoff = None
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
    SIZE = None
    WIDTH = None
    HEIGHT = None
    NVERTS = None
    TRUE = None
    FALSE = None

    def __init__(self, config_file : string):
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
                #ignore comments + blank lines
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=")
                    config[key.strip()] = value.strip()
        return config
