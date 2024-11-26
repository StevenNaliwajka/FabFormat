import json
import os

from CodeBase.config.ConfigFiles.IO_Contents.OutfileConfig.outfiles.gcode_config import GCodeFile
from CodeBase.config.ReadConfig.ReadConfigMethods.Output.handle_gcode_out import handle_gcode_out
from CodeBase.fileIO.Output.OutputTypes.GCode.gcode_nozzle import GcodeNozzle


def read_output_config(output_config):
    directory = output_config.outfile_directory_path

    # Calls all config_file readers.
    handle_gcode_out(directory, output_config)
