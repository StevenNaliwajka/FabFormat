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
import sys

from CodeBase.HandlerFiles.gui_handler import Gui_Handler
from CodeBase.DataStructure.config_data import Config_Data
from CodeBase.DataStructure.gui_data import GUI_Data

if __name__ == "__main__":
    infileDirectoryPath = sys.argv[1]
    outfileDirectoryPath = sys.argv[2]

    #Create the TK GUI
    #Reads config_file_name & stores ALL of the data for the conversion.
    CONFIG = Config_Data(infileDirectoryPath, outfileDirectoryPath)
    # Reads infile and updates config
    #INFILE = Infile_Handler()
    # Creates the GUI
    GUI_data = GUI_Data()
    GUI = Gui_Handler(CONFIG,GUI_data)

'''
boundary = []
toolpath = []
itoolpath = []
infile = []
segplot = []
vias = []
'''