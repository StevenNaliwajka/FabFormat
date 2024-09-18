# originally by:
# (C)BA Neil Gershenfeld
# commercial sale licensed by MIT
#
# modified by:
# tedgrosch
# on Apr 2, 2017
#
# Re-written and modified by Steven Naliwajka
# 9/12/2024
import os


if __name__ == "__main__":
    # 'config.txt' is a text document that contains the Excellon & Drill files to convert.
    # Also contains the details for the printer that the file will be printed on.
    # --- EX: config.txt  -------
    #  outputType = gcode
    #  xoff = 0
    #  yoff = 0
    #  size = .1
    #  undercut = 1
    #
    #  PowerMeter.cmp
    #  PowerMeter.drd
    #  PowerMeter.otl
    #  PowerMeter.sol
    # ---------------------------  THIS HAS TO BE UPDATED ONCE FINALIZED

    # --- EX: Folder format ------
    # -InputFiles
    #   - PowerMeter
    #     - config.txt
    #     - PowerMeter.cmp
    #     - PowerMeter.drd
    #     - PowerMeter.otl
    #     - PowerMeter.sol
    #   - PowerMeter2
    #     - config.txt
    #     - PowerMeter2.cmp
    #     - PowerMeter2.drd
    #     - PowerMeter2.otl
    #     - PowerMeter2.sol
    #
    # -OutputFiles
    #   - PowerMeter.gcode
    #   - PowerMeter2.gcode
    #
    # cam2.py
    # ----------------------------

    # Generates file paths.
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    parent_dir = os.path.dirname(current_dir)

    # Generates the File Path of Cam2.
    cam2FilePath = os.path.join(parent_dir, "CodeBase", "cam2.py")

    # Generates the File Path of each infile bundle.
    input1Folder = "PowerMeter"
    inputDirectoryPath = os.path.join(current_dir, "InputFiles", input1Folder)

    # Generates the File Path of where to send completed files
    outputDirectoryPath = os.path.join(current_dir, "OutputFiles")

    #Standard Usage, Can be called as many times as wanted.
    os.system(f'py {cam2FilePath} {inputDirectoryPath} {outputDirectoryPath}')
    # Calls the files
    #os.system(f'py {cam2FileLocation} {infileFileLocation} {xoff} {yoff} {size} {outfile} {undercut}')