import os
import string
from datetime import date


class Config:
    # Config Data

    def __init__(self, infileDirectoryPath: string, outfileDirectoryPath: string):

        #Input file list, populated by read_input_config.
        self.inputFileList = []

        # Default directorys provided by user on run.
        self._infileDirectoryPath = infileDirectoryPath
        self._outfileDirectoryPath = outfileDirectoryPath
        # Generates paths
        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)
        parent_dir = os.path.dirname(current_dir)

        # Generates path of GUI CONFIG
        gui_config_path = os.path.join(parent_dir, "CodeBase", "../gui_config.txt")

        # Generates path of INFILE CONFIG
        infile_config_path = os.path.join(self._infileDirectoryPath, "config.txt")

        # Generates  path of OutputFile
        self.output_path = os.path.join(self._outfileDirectoryPath)

        #Gets date for GUI
        self._date = date.today()

        #Variables set inside of the GUI_CONFIG
        self.window = None
        #Varables set inside of user CONFIG.
        self.scale = None
        self.gscale = None  # assuming gerber is in inches and scad must be in mm
        self.sthickness = None  # substrate thickness
        self.mthickness = None  # metal thickness in inches 0.19mm
        self.mwidth = None  # conductor width in inches 0.25mm
        self.size = None
        self.xoff = None
        self.yoff = None
        self.undercut = None  # Squish of filament
        self.outfile_type = None
        self.gui_state = None
        self.outfile_name = None

        #Find a better way to organize these values...
        self.feed = None
        self.spindle = None
        self.tool = None
        self.ztop = None
        self.zbottom = None


        # Reads in GUI CONFIG + Updates above registers
        self.update_config_handler(self.read_gui_config(gui_config_path), gui_config_path)
        # Reads in INPUT CONFIG + Updates above registers
        self.update_config_handler(self.read_input_config(infile_config_path), infile_config_path)


        # Variables that are used in the creation of the finished file. Stored here while compiled.
        self.infile = None
        self.list = None
        self.outfile = None
        self.type = None
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
                try:
                    #Checks if the config values can be converted to int/float before setting equal to str.
                    value = self.convert_to_number(value)
                    setattr(self, key, value)
                    #print(f"{key} successfully set to {value}")
                except AttributeError as e:
                    print(f"CONFIG_Data: Error setting {key}: {e}")
            else:
                print(f"Config Handler: {config_path} is built incorrectly, {key} is incorrectly configured.")

    def convert_to_number(self, value):
        try:
            # Try converting to int first
            return int(value)
        except ValueError:
            try:
                # If that fails, try converting to float
                return float(value)
            except ValueError:
                # If neither conversion works, return the original string
                return value

    # GETTERS --------------------------
    '''
    @property
    def window(self):
        return self._window

    @vias.setter
    def vias(self, vias):
        self._vias = vias
        
    '''
