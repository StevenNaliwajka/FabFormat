from CodeBase.InputTypes.read_dxf import ReadDxf
from CodeBase.InputTypes.read_gerber import ReadGerber
from CodeBase.OutputTypes.write_gcode import WriteGcode
from CodeBase.InputTypes.read_excellon import ReadExcellon
from CodeBase.config import Config


def input_manager(infile_path,CONFIG:Config):
    in_switcher = {
        "dxf": ReadDxf(infile_path),
        "cmp": ReadGerber(infile_path),
        "sol": ReadGerber(infile_path),
        "otl": ReadGerber(infile_path),
        #"plc": ReadGerber(infile_path), # UNKNOWN IF WORK. LISTED AS FUNTIONALITY TESTING REQ
        "drl": ReadExcellon(infile_path),
        "drd": ReadExcellon(infile_path) # An alt version of drl naming? Prof gave me drd file. Internet says drl.
    }

    # Parses file path to only get extension
    filename = infile_path.split(".")[-1]
    # Returns object of type specified.
    new_input = in_switcher.get(filename)
    # Interprets file, some-times CONFIG is required...
    try:
        new_input.path = new_input.read()
    except TypeError:
        new_input.path = new_input.read(CONFIG)
    return new_input


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


## CREATES OBJECT RETURNS IT> THEN GUI IS CREATED>>> THEN THE CODE EXECUTES OBJECT.WRITE()
