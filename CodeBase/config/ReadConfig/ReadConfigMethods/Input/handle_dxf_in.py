# Function to handle DXF files
import os

from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.infiles.dxf_config import DXFFile
from CodeBase.config.ReadConfig.ReadConfigMethods.Input.SupportMethods.parse_layer_string import parse_layer_string


def handle_dxf_in(files, input_config):
    for file_group in files:
        for file_name, attributes in file_group.items():
            print(f"Processing DXF file: {file_name}")
            file_path = os.path.join(input_config.infile_directory_path, file_name)
            file_type = attributes[0]  # e.g., "additive"
            file_level = attributes[1]  # e.g., "1"
            parsed_file_level = parse_layer_string(file_level)
            new_file = DXFFile(file_path, file_type, file_name, parsed_file_level)
            input_config.infile_list.append(new_file)
