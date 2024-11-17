from math import *
from CodeBase.gui.gui import Gui
from CodeBase.fileIO.universal_parent import UniversalParent
from CodeBase.config.config import Config


# Contains Universal Methods for converting files.

class OutputParent(UniversalParent):
    def __init__(self):
        super().__init__()

    def write_gui(self,  *args, **kwargs):
        # IMPLEMENTED by the write_xxxx.py file
        # Called IF CONFIG.gui_state == true
        pass

    def write_headless(self, *args, **kwargs):
        # IMPLEMENTED by the write_xxxx.py file
        # Called if CONFIG.gui_state != true
        pass
