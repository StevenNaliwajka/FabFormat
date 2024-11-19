import json
import os

from CodeBase.config.ConfigFiles.Files.InfileConfig.infiles.gerber_config import GerberFile


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

    # Parsing input files
    input_files = data.get("input_files", {})
    for file_type, files in input_files.items():
        print(f"\nHandling {file_type} files:")
        if file_type == "gerber":
            handle_gerber(files, input_config)
        elif file_type == "dxf":
            handle_dxf(files, input_config)
        elif file_type == "excellon_drill":
            handle_excellon_drill(files, input_config)
        else:
            raise FileNotFoundError(f"Unknown file type: {file_type}")


def handle_gerber(files, input_config):
    for file_group in files:
        for file_name, attributes in file_group.items():
            file_path = os.path.join(input_config.infile_directory_path, file_name)
            file_type = attributes[0]  # e.g., "additive"
            file_level = attributes[1]  # e.g., "1"
            new_file = GerberFile(file_path, file_type, file_name, file_level)
            input_config.infiles.append(new_file)


# Function to handle DXF files
def handle_dxf(files, input_config):
    for file_group in files:
        for file_name, attributes in file_group.items():
            file_path = os.path.join(input_config.infile_directory_path, file_name)
            file_type = attributes[0]  # e.g., "additive"
            file_level = attributes[1]  # e.g., "1"
            new_file = GerberFile(file_path, file_type, file_name, file_level)
            input_config.infiles.append(new_file)


# Function to handle Excellon drill files
def handle_excellon_drill(files, input_config):
    # DO THIS GUY
    for file_group in files:
        for file_name, drill_details in file_group.items():
            print(f"Processing Excellon Drill file: {file_name}")
            for drill, attributes in drill_details[0].items():
                drill_type = attributes[0]  # e.g., "exclusive"
                drill_level = attributes[1]  # e.g., "1-2"
                print(f"  Drill: {drill}, Type: {drill_type}, Level: {drill_level}")
