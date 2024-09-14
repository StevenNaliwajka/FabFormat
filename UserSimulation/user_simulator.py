# import GTG
import os

if __name__ == "__main__":
    #User's input
    infile = "infile.txt"
    xoff = 0
    yoff = 0
    size = .1
    outfile = "finaloutput"
    undercut = 1

    #Generates the Path of Cam2.
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    parent_dir = os.path.dirname(current_dir)
    cam2location = os.path.join(parent_dir, "CodeBase", "cam2.py")

    os.system(f'py {cam2location} {infile} {xoff} {yoff} {size} {outfile} {undercut}')

    #os.system('py C:\\Users\Kevin\PycharmProjects\Gerber-DrilltoGcode\CodeBase\cam2.py %s %s %s %s %s %s' % (infile, xoff, yoff, size, outfile, undercut))
