import json
import os

from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.infiles.dxf_config import DXFFile
from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.infiles.excellon_config import ExcellonFile
from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.infiles.gerber_config import GerberFile
from CodeBase.config.ReadConfig.ReadConfigMethods.Input.handle_dxf_in import handle_dxf_in
from CodeBase.config.ReadConfig.ReadConfigMethods.Input.handle_excellon_drill_in import handle_excellon_drill
from CodeBase.config.ReadConfig.ReadConfigMethods.Input.handle_gerber_config_in import handle_gerber


def read_input_config(input_config):
    directory = input_config.infile_directory_path
    file_path = os.path.join(directory, "input_config.json")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"\"input_config.json\" not found, copy a input_config file from codebase and re-run")

    with open(file_path, 'r') as file:
        data = json.load(file)

    # load GUI State
    input_config.gui_state = data["gui_state"]
    # load input file path
    input_config.infile_directory_path = data["infile_directory_path"]
    # load output directory path
    input_config.outfile_directry_path = data["outfile_directry_path"]

    # Parsing input files
    input_files = data.get("input_files", {})
    for file_type, files in input_files.items():
        print(f"\nHandling {file_type} files:")
        if file_type == "gerber":
            handle_gerber(files, input_config)
        elif file_type == "dxf":
            handle_dxf_in(files, input_config)
        elif file_type == "excellon_drill":
            handle_excellon_drill(files, input_config)
        else:
            raise FileNotFoundError(f"Unknown file type: {file_type}")
