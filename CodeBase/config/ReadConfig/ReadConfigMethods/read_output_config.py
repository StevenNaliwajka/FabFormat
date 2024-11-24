import json
import os

from CodeBase.config.ConfigFiles.IO_Contents.OutfileConfig.outfiles.gcode_config import GCodeFile
from CodeBase.fileIO.Output.OutputTypes.GCode.gcode_nozzle import GcodeNozzle


def read_output_config(output_config):
    directory = output_config.outfile_directory_path

    # Calls all config_file readers.
    handle_gcode_out(directory, output_config)


def handle_gcode_out(directory, output_config):
    gcode_config_path = os.path.join(directory, "gcode_output_config.json")
    if os.path.exists(gcode_config_path):
        with open(gcode_config_path, 'r') as file:
            data = json.load(file)

        for file_name, file_details in data["gcode_output_files"]:
            output_directory = file_details["output_file_directory"]
            output_path = os.path.join(output_directory, file_name, ".gcode")

            # create new gcode config
            new_gcode = GCodeFile(output_path, file_name)

            # Fill gcode config
            new_gcode.unit = file_details["unit"]
            new_gcode.gcode_flavor = file_details["gcode_flavor"]
            new_gcode.bed_temp_C = file_details["bed_temp_c"]
            new_gcode.layer_height = file_details["layer_height"]

            for nozzle_name, nozzle_details in file_details["nozzles"]:
                # Check if nozzle active.
                if nozzle_details["active"].lower() in {"t", "true"}:
                    nozzle_code = nozzle_details["nozzle_code"]
                    nozzle_size_mm = nozzle_details["nozzle_size_mm"]
                    filament_diameter_mm = nozzle_details["filament_diameter_mm"]
                    nozzle_temp_c = nozzle_details["nozzle_temp_c"]
                    cooling_fan_percent = nozzle_details["cooling_fan_%"]
                    infill_percent = nozzle_details["infill_%"]
                    print_speed = nozzle_details["print_speed_mm/s"]
                    travel_speed = nozzle_details["travel_speed_mm/s"]
                    initial_layer_speed = nozzle_details["initial_layer_speed_mm/s"]
                    retraction_distance = nozzle_details["retraction_distance_mm"]
                    retraction_speed = nozzle_details["retraction_speed_mm/s"]
                    new_nozzle = GcodeNozzle(nozzle_name, nozzle_code, nozzle_size_mm, filament_diameter_mm,
                                             nozzle_temp_c, cooling_fan_percent, infill_percent, print_speed,
                                             travel_speed, initial_layer_speed, retraction_distance, retraction_speed)
                    new_gcode.nozzle_list.append(new_nozzle)

            output_config.outfile_list.append(new_gcode)
