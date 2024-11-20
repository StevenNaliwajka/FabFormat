from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.input_parent import InputParent
from CodeBase.config.ConfigFiles.IO_Contents.file_parent import FileParent


class DXFFile(InputParent):
    def __init__(self, filepath, layer_type, file_name, active_layers):
        file_type = "dxf"
        super().__init__(filepath, file_name, file_type, layer_type, active_layers)