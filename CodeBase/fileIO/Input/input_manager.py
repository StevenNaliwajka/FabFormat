from CodeBase.fileIO.Input.InputTypes.DXF.read_dxf import ReadDxf
from CodeBase.fileIO.Input.InputTypes.Gerber.read_gerber import ReadGerber
from CodeBase.fileIO.Input.InputTypes.ExcellonDrill.read_excellon_drill import ReadExcellonDrill
from CodeBase.misc.config import Config


def input_manager(infile_path, common_form, CONFIG: Config):
    # in_switcher is a list of the supported file extension types.
    in_switcher = {
        "dxf": ReadDxf(infile_path, common_form),
        "cmp": ReadGerber(infile_path, common_form),  # Single files. Used for only copper trace
        "sol": ReadGerber(infile_path, common_form),
        "otl": ReadGerber(infile_path, common_form),
        # "plc": ReadGerber(infile_path, common_form), # UNKNOWN IF WORK. LISTED AS FUNCTIONALITY TESTING REQ
        "drl": ReadExcellonDrill(infile_path, common_form),
        "drd": ReadExcellonDrill(infile_path, common_form),  # An alt version of drl naming? Prof gave me drd file.

        # Used for "2 Layer" Boards. Converted into GERBER+EXCELLON from EAGLE>
        # BOTTOM
        "gbl": ReadGerber(infile_path, common_form),  # Bottom Copper
        "gbo": ReadGerber(infile_path, common_form),  ## DONT CARE: Silkscreen "Text or drawings on board", Possible 3rd fillament?
        "gbp": ReadGerber(infile_path, common_form),  ## DONT CARE: Bottom solder paste stencil.
        "gbs": ReadGerber(infile_path, common_form),  # Bottom solder mask.
        "gko": ReadGerber(infile_path, common_form),  # Bottom keepout. Shows where comp/traces cant be placed.
        # TOP
        "gtl": ReadGerber(infile_path, common_form),  # Top copper
        "gto": ReadGerber(infile_path, common_form),  ## DONT CARE: Silkscreen "Text or drawings on board", Possible 3rd fillament?
        "gtp": ReadGerber(infile_path, common_form),  ## DONT CARE: Bottom solder paste stencil.
        "gts": ReadGerber(infile_path, common_form),  # Top solder mask
        "xln": ReadExcellonDrill(infile_path, common_form)  # drill files. Defines Vias and through holes...

    }

    # Parses file path to only get extension. Ignores case.
    filename = infile_path.lower().split(".")[-1]
    # Returns object of type specified.
    new_input = in_switcher.get(filename)

    # Interprets file, some-times CONFIG is required...
    try:
        new_input.path = new_input.parse_into_cf()
    except TypeError:
        new_input.path = new_input.parse_into_cf(CONFIG)
    except AttributeError:
        print(f"File type \".{filename}\" not supported: See \"in_out_manager.py\" for supported file types.")
        exit()

    return new_input