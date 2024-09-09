# import GTG
import os

if __name__ == "__main__":
    infile = "infile.txt"
    xoff = 0
    yoff = 0
    size = 100
    outfile = "finaloutput"
    undercut = 1

    # GTG.py infile xoff yoff size outfile undercut

    os.system('py GTG.py %s %s %s %s %s %s' % (infile, xoff, yoff, size, outfile, undercut))
