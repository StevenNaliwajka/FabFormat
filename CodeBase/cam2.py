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
import os
import sys

from CodeBase.fileIO.CommonFormat.common_form import CommonForm
from CodeBase.fileIO.Input.input_manager import input_manager

from CodeBase.fileIO.Output.output_manager import output_manager
from CodeBase.misc.config import Config

if __name__ == "__main__":
    infileDirectoryPath = sys.argv[1]
    outfileDirectoryPath = sys.argv[2]

    # Create new config object for global slicer settings.
    config = Config(infileDirectoryPath, outfileDirectoryPath)

    # Common Form: Stores Universal File Data
    common_form = CommonForm()

    ## SWAP INFILE OBJECT LIST TO CREATE THE INFILE OBJECT inside of a method and discard it when
    ## it is done so that way more memory is not required.
    # Populates list with each infile
    input_file_obj_list = []
    for i in range(len(config.inputFileList)):
        infile_path = os.path.join(infileDirectoryPath, config.inputFileList[i])
        new_infile = input_manager(infile_path, common_form, config)
        input_file_obj_list.append(new_infile)

    print("CREATING OUTFILE")
    # Create new Output object
    outfile = output_manager(config.outfile_type)
    print("OUTFILE CREATED")
    gui = None
    if config.gui_state.lower() == "true":
        print("STARTING GUI")
        # GUI = Gui(CONFIG)
        pass
    else:
        print("STARTING HEADLESS")
        outfile.write_headless(input_file_obj_list=input_file_obj_list, config=config)
