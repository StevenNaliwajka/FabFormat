#
# cam2.py
#
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

from gui_handler import Gui_Handler
from config_handler import Config_Handler

if __name__ == "__main__":
    config_file_name = "config.txt"

    #Create the TK GUI
    CONFIG = Config_Handler(config_file_name)
    GUI = Gui_Handler(CONFIG)


boundary = []
toolpath = []
itoolpath = []
infile = []
segplot = []
vias = []