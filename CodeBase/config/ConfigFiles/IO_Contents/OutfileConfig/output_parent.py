from CodeBase.config.ConfigFiles.IO_Contents.file_parent import FileParent


class OutputParent(FileParent):
    def __init__(self, filepath, file_name, file_type, layer_type):
        # Additive/Subtractive/Outline/Exclusive
        super().__init__(filepath, file_name, file_type, layer_type)
