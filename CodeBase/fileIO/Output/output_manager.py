from CodeBase.fileIO.Output.OutputTypes.GCode.write_gcode import WriteGcode

def output_manager(outfile_type):
    out_switcher = {
        #"rml": write_rml(outfile_type),
        #"camm": write_camm(outfile_type),
        #"jpg": write_img(outfile_type),
        #"epi": write_epi(outfile_type),
        "gcode": WriteGcode()
    }
    # Returns object of type specified.
    # Note, Does not parse, GUI must be made first.
    return out_switcher.get(outfile_type)