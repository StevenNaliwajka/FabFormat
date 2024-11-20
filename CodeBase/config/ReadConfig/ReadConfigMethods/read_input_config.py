import json
import os

from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.infiles.dxf_config import DXFFile
from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.infiles.excellon_config import ExcellonFile
from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.infiles.gerber_config import GerberFile


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
            handle_dxf(files, input_config)
        elif file_type == "excellon_drill":
            handle_excellon_drill(files, input_config)
        else:
            raise FileNotFoundError(f"Unknown file type: {file_type}")


def handle_gerber(files, input_config):
    for file_group in files:
        for file_name, attributes in file_group.items():
            print(f"Processing Gerber file: {file_name}")
            file_path = os.path.join(input_config.infile_directory_path, file_name)
            file_type = attributes[0]  # e.g., "additive"
            file_level = attributes[1]  # e.g., "1"
            parsed_file_level = parse_layer_string(file_level)
            new_file = GerberFile(file_path, file_type, file_name, parsed_file_level)
            input_config.infile_list.append(new_file)


# Function to handle DXF files
def handle_dxf(files, input_config):
    for file_group in files:
        for file_name, attributes in file_group.items():
            print(f"Processing DXF file: {file_name}")
            file_path = os.path.join(input_config.infile_directory_path, file_name)
            file_type = attributes[0]  # e.g., "additive"
            file_level = attributes[1]  # e.g., "1"
            parsed_file_level = parse_layer_string(file_level)
            new_file = DXFFile(file_path, file_type, file_name, parsed_file_level)
            input_config.infile_list.append(new_file)


# Function to handle Excellon drill files
def handle_excellon_drill(files, input_config):
    # gets each excellon file
    for file_group in files:

        for file_name, drill_details in file_group.items():
            print(f"Processing Excellon Drill file: {file_name}")
            file_path = os.path.join(input_config.infile_directory_path, file_name)
            drill_layer_list = []
            drill_type_list = []
            for drill, attributes in drill_details[0].items():
                # Gets drill #
                drill_number = parse_d_number(drill)

                # Gets drill type and level
                drill_type = attributes[0]  # e.g., "exclusive"
                drill_level = attributes[1]  # e.g., "1-2"

                # Parses drill level to a list
                parsed_file_level = parse_layer_string(drill_level)

                # Adds to the lists.
                insert_with_padding(drill_layer_list, drill_number-1, parsed_file_level)
                insert_with_padding(drill_type_list, drill_number - 1, drill_level)
                # print(f"  Drill: {drill}, Type: {drill_type}, Level: {drill_level}")

            # Creates new excellon file.
            new_file = ExcellonFile(file_path, drill_layer_list, file_name, drill_type_list)
            input_config.infile_list.append(new_file)


def parse_layer_string(input_string):
    if '-' in input_string and ',' not in input_string:  # Case 3: Range format
        start, end = map(int, input_string.split('-'))
        return list(range(start, end + 1))  # Return a list of numbers in the range
    elif ',' in input_string:  # Case 2: Comma-separated format
        return [int(num.strip()) for num in input_string.split(',')]  # Return a list of numbers
    else:  # Case 1: Single number
        return [int(input_string.strip())]  # Return a single number as a list


def parse_d_number(input_string):
    if input_string.startswith('d'):
        return int(input_string[1:])  # Extract everything after 'd' and convert to an integer
    else:
        raise ValueError("Input string does not start with 'd'")


def insert_with_padding(my_list, index, value):
    if index >= len(my_list):  # If the index is out of bounds
        # Extend the list with None until the designated index
        my_list.extend([None] * (index - len(my_list)))
        my_list.append(value)  # Add the value at the end
    else:
        my_list.insert(index, value)  # Insert the value if within bounds
