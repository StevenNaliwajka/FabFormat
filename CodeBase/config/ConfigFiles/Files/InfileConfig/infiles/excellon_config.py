from CodeBase.config.ConfigFiles.Files.file_parent import FileParent


class ExcellonFile(FileParent):
    def __init__(self, filepath, layer_type, file_name, active_layers):
        file_type = "excellon"
        super().__init__(filepath, layer_type, file_name, file_type, active_layers)
        # Create variable here that allows for drill data to be stored. 2D? or 1D, but [0] = drill 1. etc.
