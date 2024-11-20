from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.input_parent import InputParent
from CodeBase.config.ConfigFiles.IO_Contents.file_parent import FileParent


class GerberFile(InputParent):
    def __init__(self, filepath, file_name, layer_type, active_layers):
        file_type = "gerber"
        super().__init__(filepath, file_name, file_type, layer_type, active_layers)
