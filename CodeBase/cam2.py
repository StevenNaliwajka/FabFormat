#
# cam2.py
#
#THIS INFO HAS MODIFIED
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
import os
import sys
from CodeBase.config import Config
from CodeBase.in_out_manager import *
from CodeBase.gui import Gui

if __name__ == "__main__":
    infileDirectoryPath = sys.argv[1]
    outfileDirectoryPath = sys.argv[2]

    # Create new config object for global slicer settings.
    CONFIG = Config(infileDirectoryPath, outfileDirectoryPath)

    # Populates list with each infile
    input_file_obj_list = []
    for i in range(len(CONFIG.inputFileList)):
        infile_path = os.path.join(infileDirectoryPath, CONFIG.inputFileList[i])
        new_infile = input_manager(infile_path,CONFIG)
        input_file_obj_list.append(new_infile)
    print("CREATING OUTFILE")
    # Create new Output object
    outfile = output_manager(CONFIG.outfile_type)
    print("OUTFILE CREATED")
    GUI = None
    if CONFIG.gui_state.lower() == "true":
        print("STARTING GUI")
        # GUI = Gui(CONFIG)
        pass
    else:
        print("STARTING HEADLESS")
        outfile.write_headless(CONFIG=CONFIG, path=input_file_obj_list[0].path)

