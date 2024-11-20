from CodeBase.config.ConfigFiles.IO_Contents.file_parent import FileParent


class InputParent(FileParent):
    def __init__(self, filepath, file_name, file_type, layer_type, active_layers):
        # Additive/Subtractive/Outline/Exclusive
        super().__init__(filepath, file_name, file_type, layer_type)
        # 1/2/3/... or A for ALL
        self.active_layers = active_layers
