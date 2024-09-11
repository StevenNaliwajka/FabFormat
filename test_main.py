# import GTG
import os

if __name__ == "__main__":
    infile = "infile.txt"
    xoff = 0
    yoff = 0
    size = .1
    outfile = "finaloutput"
    undercut = 1

    # GTG.py infile xoff yoff size outfile undercut

    #os.system(f'py GTG.py {infile} {xoff} {yoff} {size} {outfile} {undercut}')
    os.system('py cam1.py %s %s %s %s %s %s' % (infile, xoff, yoff, size, outfile, undercut))
