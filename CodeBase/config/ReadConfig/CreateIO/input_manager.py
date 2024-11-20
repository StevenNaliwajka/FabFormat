import os

from CodeBase.fileIO.Input.InputTypes.DXF.read_dxf import ReadDxf
from CodeBase.fileIO.Input.InputTypes.Gerber.read_gerber import ReadGerber
from CodeBase.fileIO.Input.InputTypes.ExcellonDrill.read_excellon_drill import ReadExcellonDrill


def read_infiles(infile_config, common_form):
    input_file_obj_list = []
    new_input = None
    for config in infile_config.infile_list:
        if config.file_type == "gerber":
            new_input = ReadGerber(config, common_form)
        elif config.file_type == "excellon_drill":
            new_input = ReadExcellonDrill(config, common_form)
        elif config.file_type == "dxf":
            new_input = ReadDxf(config, common_form)
        input_file_obj_list.append(new_input)
    return input_file_obj_list


def convert_infiles_to_common_form(input_file_obj_list):
    for infile in input_file_obj_list:
        # Converts file to GCODE.
        infile.path = infile.parse_into_cf()