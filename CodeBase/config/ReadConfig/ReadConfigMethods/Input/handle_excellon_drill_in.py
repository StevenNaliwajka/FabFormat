# Function to handle Excellon drill files
import os

from CodeBase.config.ConfigFiles.IO_Contents.InfileConfig.infiles.excellon_config import ExcellonFile
from CodeBase.config.ReadConfig.ReadConfigMethods.Input.SupportMethods.parse_layer_string import parse_layer_string


def handle_excellon_drill_in(files, input_config):
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