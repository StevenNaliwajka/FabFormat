from math import *
from CodeBase.gui.gui import Gui
from CodeBase.fileIO.universal_parent import UniversalParent
from CodeBase.config.config import Config
from abc import abstractmethod

# Contains Universal Methods for converting files.

class OutputParent(UniversalParent):
    def __init__(self, file_path, unit, common_form):
        super().__init__(file_path, common_form)
        self.unit = unit

    @abstractmethod
    def write_gui(self,  *args, **kwargs):
        # IMPLEMENTED by the write_xxxx.py file
        # Called IF CONFIG.gui_state == true
        pass

    @abstractmethod
    def write_headless(self, *args, **kwargs):
        # IMPLEMENTED by the write_xxxx.py file
        # Called if CONFIG.gui_state != true
        pass

    def _verify_units_in_cf_list(self, list_of_cf):
        for cf in list_of_cf:
            if cf.unit.lower() in {"in, i, inches"}:
                if self.unit.lower() in {"in, i, inches"}:
                    pass
                elif self.unit.lower() in {"mm"}:
                    cf.change_unit("mm")
            elif cf.unit.lower() in {"mm"}:
                if self.unit.lower() in {"mm"}:
                    pass
                elif self.unit.lower() in {"in, i, inches"}:
                    cf.change_unit("inches")
