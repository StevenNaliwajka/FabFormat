class FileParent:
    def __init__(self, filepath, layer_type, file_name, file_type, active_layers):
        # Filepath
        self.filepath = filepath
        # Filename + Extension
        self.file_name = file_name
        # FileType
        self.file_type = file_type
        # Additive/Subtractive/Outline/Exclusive
        self.layer_type = layer_type
        # 1/2/3/... or A for ALL
        self.active_layers = active_layers
