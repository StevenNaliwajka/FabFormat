from CodeBase.config.ConfigFiles.IO_Contents.file_parent import FileParent


class GCodeFile(FileParent):
    def __init__(self, filepath, file_name):
        file_type = "gcode"
        super().__init__(filepath, file_name, file_type)
        self.unit = None
        self.gcode_flavor = None
        self.bed_temp_C = None
        self.layer_height_mm = None
        self.nozzle_list = []