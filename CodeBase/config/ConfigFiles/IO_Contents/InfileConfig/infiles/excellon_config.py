from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.input_parent import InputParent
from CodeBase.config.ConfigFiles.IO_Contents.file_parent import FileParent


class ExcellonFile(InputParent):
    def __init__(self, filepath, layer_type, file_name, active_layers):
        file_type = "excellon_drill"
        super().__init__(filepath, file_name, file_type, layer_type, active_layers)

        # drill data stored as list in file_type and active_layers,
        # d1 = [0], d2 = [1], etc...
        # file_type = ["additive", "subtractive", "exclusive", ...]
        # active_layers = [[0], [3,4,5], [0,1,2,3], ...]
