from CodeBase.config.ConfigFiles.IO_Contents.file_parent import FileParent


class OutputParent(FileParent):
    def __init__(self, filepath, file_name, file_type):
        # Additive/Subtractive/Outline/Exclusive
        super().__init__(filepath, file_name, file_type)

        # output_material_has_depth
        self.output_material_has_depth = None

        # generate_core_bounded_by_outline
        self.generate_core_bounded_by_outline = None

        # list of active trace types and their tool
        # stored as touple (layer_type, tool)
        self.active_trace_types = None

        self.annotation_flag = False

    def new_active_type(self, layer_type, tool):
        # check if int.
        if not isinstance(tool, int):
            raise ValueError(f"{tool} is not an int.")

        if layer_type in {"primary", "subtractive", "core", "annotation"}:
            self.active_trace_types.append((layer_type, tool))
        else:
            raise ValueError(f"LayerType: {layer_type} not recognized, check config.")

        if layer_type == "annotation":
            self.annotation_flag = True
