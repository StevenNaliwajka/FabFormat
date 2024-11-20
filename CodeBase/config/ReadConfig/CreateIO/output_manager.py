from CodeBase.fileIO.Output.OutputTypes.GCode.write_gcode import WriteGcode


def get_outfiles(output_config, common_form):
    output_file_obj_list = []
    new_output = None
    for config in output_config.outfile_list:
        if config.file_type == "gcode":
            new_output = WriteGcode(config, common_form)
        output_file_obj_list.append(new_output)
    return output_file_obj_list
