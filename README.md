# IN PROG: 100% by Nov 29 (70%:Oct 25)
The cumulation of a semester of work for my senior project "Affordable 3D PCB Printing for Prototyping".

Goal is to have a modular file converter and slicer. 
So that PCBs can be printed on a standard dual extrusion FDM 3D printer using conductive fillament in place of copper.
Components can be surface mounted by hand using conductive epoxy. 
While any number of input layers are allowed, embedded components are not supported.

Inspriation gained from BA Neil Gershenfeld (GTG.py) and my professor Theodore Grosch (cam1.py).
Even though I think I have rewritten every inherited code block, I could not have gotten this far without their prior work.

---------------------------------------------------------------------------------------------------------

CodeFlow:

1)Using a config file based approach, a user adds any number of supported input file types: 
   - Excellon Drill
   - Gerber

2)Infiles are read in and converted and stored in a common format.

3)This is then converted to a single supported output file type: 
   - Gcode
   - PNG

Its not completed 100%, more like 70%. Infiles -> Common form is done. Common form -> 2 extruder Gcode is in the works.   


Notes:
- Currently Headless mode is only supported, had to drop Gershenfeld's GUI when refactoring to opject oriented.
- Modular so adding new input or output file types is as easy as converting to or from common form.
- I *think* all modern gerber features are supported. AM(aperture macros) etc.. more testing required to be sure.

---------------------------------------------------------------------------------------------------------


### Folders:
Codebase
    - Rewritten code files: "cam2.py" is my rewritten slicer.

OGCodeFiles
    - Basis from (C)BA Neil Gershenfeld (GTG.py) and Theodore Grosch (cam1.py).

UserSimulation
    - Testing, simulates a user running cam2.py from CodeBase
