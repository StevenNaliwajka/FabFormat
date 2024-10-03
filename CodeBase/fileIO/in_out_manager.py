from CodeBase.fileIO.InputTypes.read_dxf import ReadDxf
from CodeBase.fileIO.InputTypes.read_gerber import ReadGerber
from CodeBase.fileIO.OutputTypes.write_gcode import WriteGcode
from CodeBase.fileIO.InputTypes.read_excellon import ReadExcellon
from CodeBase.misc.config import Config


def input_manager(infile_path, CONFIG: Config):

    # in_switcher is a list of the supported file extension types.
    in_switcher = {
        "dxf": ReadDxf(infile_path),
        "cmp": ReadGerber(infile_path),  # Single files. Used for only copper trace
        "sol": ReadGerber(infile_path),
        "otl": ReadGerber(infile_path),
        # "plc": ReadGerber(infile_path), # UNKNOWN IF WORK. LISTED AS FUNCTIONALITY TESTING REQ
        "drl": ReadExcellon(infile_path),
        "drd": ReadExcellon(infile_path),  # An alt version of drl naming? Prof gave me drd file. Internet says drl.

        # Used for "2 Layer" Boards. Converted into GERBER+EXCELLON from EAGLE>
        # BOTTOM
        "gbl": ReadGerber(infile_path),  # Bottom Copper
        "gbo": ReadGerber(infile_path),  ## DONT CARE: Silkscreen "Text or drawings on board", Possible 3rd fillament?
        "gbp": ReadGerber(infile_path),  ## DONT CARE: Bottom solder paste stencil.
        "gbs": ReadGerber(infile_path),  # Bottom solder mask.
        "gko": ReadGerber(infile_path),  # Bottom keepout. Shows where comp/traces cant be placed.
        # TOP
        "gtl": ReadGerber(infile_path),  # Top copper
        "gto": ReadGerber(infile_path),  ## DONT CARE: Silkscreen "Text or drawings on board", Possible 3rd fillament?
        "gtp": ReadGerber(infile_path),  ## DONT CARE: Bottom solder paste stencil.
        "gts": ReadGerber(infile_path),  # Top solder mask
        "xln": ReadExcellon(infile_path)  # drill files. Defines Vias and through holes...

    }

    # Parses file path to only get extension. Ignores case.
    filename = infile_path.lower().split(".")[-1]
    # Returns object of type specified.
    new_input = in_switcher.get(filename)


    # Interprets file, some-times CONFIG is required...
    try:
        new_input.path = new_input.read()
    except TypeError:
        new_input.path = new_input.read(CONFIG)
    except AttributeError:
        print(f"File type \".{filename}\" not supported: See \"in_out_manager.py\" for supported file types.")
        exit()
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
