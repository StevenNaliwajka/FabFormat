## SHOULD BE NOTED AS NOT WORKING YET... IN PROG
I was provided a python file "cam1.py" by my professor Theodore Grosch.

Prof. Grosch created "cam1.py" from Neil Gershenfeld's script "GTG.py".

Definition of standing on the shoulders of giants.

This project has a few steps.
1) Put a better front end on the code so, it is easier scalable for bulk execution and allows for headless.
   1) Config based approach. Headless currently works. Gonna get the combining of files working before gui.
2) Format "cam1.py": break it down into similar subfiles.
   1) Broken down. Object oriented and scalable. Nice.
3) Once "cam1.py" has been digested, debug the outputs.
   1) Done. Can slice single files and outputs a usable gcode file.
   2) So far used default gerber parser (no issues). Have updated the Excellion parser to work better.
   2) RN, working on how the best way to merge the copper and insulator files to be able to print on a dual extruder FDM printer.
   3) I realize a lot of values were hard coded. These need to be extracted and placed into config. (eg. nozzle settings, bed heat. etc...)
   4) Still digging through understanding how the 'cam1.py' handled itself so I can splice together two or more files...
# Gerber-DrilltoGcode
A project to convert gerber and drill files to gcode for "Affordable 3D printed PCB's for prototyping" senior project.

Prog goal is to leave it scalable so its 'easy' to add differnt output file types, input file types for future use cases.

### Folders:
Codebase
    - Rewritten code files: "cam2.py" is my rewritten slicer.

OGCodeFiles
    - Basis from (C)BA Neil Gershenfeld (GTG.py) and Theodore Grosch (cam1.py).

UserSimulation
    - Testing, simulates a user running cam2.py from CodeBase
