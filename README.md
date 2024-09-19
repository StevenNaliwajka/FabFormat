## SHOULD BE NOTED AS NOT WORKING YET...
I was provided a python file "cam1.py" by my professor Theodore Grosch.

Prof. Grosch created "cam1.py" from Neil Gershenfeld's script "GTG.py".

Definition of standing on the shoulders of giants. Reportedly the "cam1.py" file is 90% of the way there.
All that is left is debugging.

This micro-project has a few steps.
1) Put a better front end on the code so, it is easier scalable for bulk execution.
   1) DONE. See the user_simulator for a use case scenario.
2) Format "cam1.py": break it down into similar subfiles.
   1) In prog. See Handler files.
3) Once "cam1.py" has been digested, debug the outputs.

# Gerber-DrilltoGcode
A project to convert gerber and drill files to gcode for "Affordable 3D printed PCB's for prototyping" senior project.

Prog goal is to leave it scalable so its 'easy' to add differnt output file types, input file types for future use cases.

### Folders:
Codebase
    - Rewritten code files: "cam2.py" is my rewritten converter.

OGCodeFiles
    - Basis from (C)BA Neil Gershenfeld (GTG.py) and Theodore Grosch (cam1.py).

UserSimulation
    - Testing, simulates a user running cam2.py from CodeBase