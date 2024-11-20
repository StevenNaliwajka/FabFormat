#
# cam2.py
#
# THIS INFO HAS MODIFIED
# usage: python cam2.py [infile] [xoffset yoffset] [display size] [outfile] [undercut]
#
# input:
#     *.dxf: DXF (polylines)
#     *.cmp,*.sol,*.plc: Gerber
#         RS-274X format, with 0-width trace defining board boundary
#     *.drl: Excellon drill file, with tool defitions
# output:
#     *.rml: Roland Modela RML mill
#     *.camm: Roland CAMM cutter
#     *.jpg,*.bmp: images
#     *.epi: Epilog lasercutter
#     *.g: G codes
# toolpath modes: 1D path, contour, raster
# keys: q to quit
# originally by:
# (C)BA Neil Gershenfeld
# commercial sale licensed by MIT
#
# modified by
# tedgrosch
# on Apr 2, 2017
#
# Updated
# 9/12/2024


# FOR MYSELF:
# Showcase multi layer circuits w/
# Converting GCODE + Excellon-Drill into COMMON FORMAT *MADE UP NAME BY ME*
# CF(COMMON FORMAT) HAS TWO PARTS. ADDATIVE (EX: COPPER TRACES), SUBTRACTIVE (DRILL)
# CF/ADDATIVE IS A LIST OF OBJECTS. OBJECTS REPRESENT LAYERS. EACH OBJECT CONTAINS LIST OF EACH 'line' or 'curve'
# on that layer.
# CF/SUBTRACTIVE is a list and a DICT. List is of drill sizes. DICT is a list of the holes that each drill makes.
# CURRENTLY! IT IS UP TO USER TO DETERMINE IN CONFIG WHETHER A DRILL RESULTS IN A HOLE or a blind/buried/through via.

# AFTER CF IS ACHEIVED. THE SUBTRACTIVE + ADDATIVE PARTS ARE MERGED INTO ONE GCODE FILE. LAYER BY LAYER
# THIS CAN BE DONE BY RAW MIN/MAX OF THE FILE TO RESULT IN SQUARE OR USING AN OUTLINE FILE PROVIDED.
# MUST TAKE INTO CONSIDERATION PRINTING CONDUCTIVE PLASTIC WITH NOZZLE #1 AND NON-CONDUCTIVE PLASTIC WITH NOZZLE #2
# FOR NOW.. 100% INFIL. NOT MY PROBLEM TO BE CONSERVITAVE WITH NON CONDUCTIVE FILLAMENT TILL IT WORKS.
import sys

from CodeBase.config.ReadConfig.CreateIO.input_manager import read_infiles, convert_infiles_to_common_form
from CodeBase.config.ReadConfig.CreateIO.output_manager import get_outfiles
from CodeBase.config.ReadConfig.main_config_read import main_config_read
from CodeBase.fileIO.CommonFormat.common_form import CommonForm

if __name__ == "__main__":
    print("FabFormat")
    print("Created by Steven Naliwajka")
    infile_directory_path = sys.argv[1]
    #outfile_directory_path = sys.argv[2]

    # Read in Config Files
    gui_config, input_config, output_config = main_config_read(infile_directory_path)

    ## Create new config object for global slicer settings.
    #config = Config(infile_directory_path, outfile_directory_path)

    # Common Form: Stores Universal File Data
    common_form = CommonForm(input_config, output_config)

    # Creat infile objects
    # Populates list with each infile obj
    input_file_obj_list = read_infiles(input_config, common_form)

    # Converts infiles in list to Common Form
    convert_infiles_to_common_form(input_file_obj_list)

    output_file_obj_list = get_outfiles(output_config, common_form)

    # Generate core traces and handle subtractive traces depending on what output forms have been chosen.
    common_form.format_layers()

    if gui_config is not None:
        print("STARTING GUI")
        # GUI = Gui(CONFIG)
        pass
        ## GUI NOT SUPPORTED YET
    else:
        print("STARTING HEADLESS")
        for file in output_file_obj_list:
            common_form.verify_units(file)
            file.write_headless()
