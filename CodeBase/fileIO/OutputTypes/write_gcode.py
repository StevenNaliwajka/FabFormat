import os

from CodeBase.fileIO.OutputTypes.output_parent import OutputParent
from CodeBase.misc.config import Config
from CodeBase.misc.gui import Gui

class WriteGcode(OutputParent):
    def __init__(self):
        super().__init__()

    def write_headless(self, input_file_obj_list, CONFIG:Config):
        #
        # Gerber code output
        #


        print("WRITINGNOW")
        scale = CONFIG.scale
        xoff = CONFIG.xoff
        yoff = CONFIG.yoff
        outfile_directory = CONFIG.output_path
        outfile_full_name = (f"{CONFIG.outfile_name}.{CONFIG.outfile_type}")
        outfile_path = os.path.join(outfile_directory, outfile_full_name)
        file = open(outfile_path, 'w')
        file.write("G90\n")  # absolute positioning
        file.write("F" + str(CONFIG.feed) + "\n")  # feed rate
        file.write("S" + str(CONFIG.spindle) + "\n")  # spindle speed
        file.write("T" + str(CONFIG.tool) + "\n")  # tool
        file.write("M08\n")  # coolant on
        file.write("M03\n")  # spindle on clockwise
        for i in input_file_obj_list:
            print(f"I is :{i}")
            path = input_file_obj_list[i].path
            for segment in range(len(path)):
                vertex = 0
                x = path[segment][vertex][self.X] * scale + xoff
                y = path[segment][vertex][self.Y] * scale + yoff
                file.write("G00X%0.4f" % x + "Y%0.4f" % y + "Z" + str(CONFIG.ztop) + "\n")  # rapid motion
                file.write("G01Z" + str(CONFIG.zbottom) + "\n")  # linear motion
                for vertex in range(1, len(path[segment])):
                    x = path[segment][vertex][self.X] * scale + xoff
                    y = path[segment][vertex][self.Y] * scale + yoff
                    file.write("X%0.4f" % x + "Y%0.4f" % y + "\n")
                file.write("Z" + str(CONFIG.ztop) + "\n")
            file.write("M05\n")  # spindle stop
            file.write("M09\n")  # coolant off
            file.write("M30\n")  # program end and reset
            file.close()
            print("wrote", len(path), "G code toolpath segments to", outfile_path)


    def write_gui(self, input_file_obj_list, GUI:Gui):
        #
        # G code output
        #

        ## GET PATH FROM input_file_obj_list
        scale = float(GUI.sscale.get())
        xoff = float(GUI.sxoff.get())
        yoff = float(GUI.syoff.get())
        text = GUI.outfile.get()
        file = open(text, 'w')
        file.write("G90\n")  # absolute positioning
        file.write("F" + GUI.sfeed.get() + "\n")  # feed rate
        file.write("S" + GUI.sspindle.get() + "\n")  # spindle speed
        file.write("T" + GUI.stool.get() + "\n")  # tool
        file.write("M08\n")  # coolant on
        file.write("M03\n")  # spindle on clockwise
        for segment in range(len(path)):
            vertex = 0
            x = path[segment][vertex][self.X] * scale + xoff
            y = path[segment][vertex][self.Y] * scale + yoff
            file.write("G00X%0.4f" % x + "Y%0.4f" % y + "Z" + GUI.sztop.get() + "\n")  # rapid motion
            file.write("G01Z" + GUI.szbottom.get() + "\n")  # linear motion
            for vertex in range(1, len(path[segment])):
                x = path[segment][vertex][self.X] * scale + xoff
                y = path[segment][vertex][self.Y] * scale + yoff
                file.write("X%0.4f" % x + "Y%0.4f" % y + "\n")
            file.write("Z" + GUI.sztop.get() + "\n")
        file.write("M05\n")  # spindle stop
        file.write("M09\n")  # coolant off
        file.write("M30\n")  # program end and reset
        file.close()
        print("wrote", len(path), "G code toolpath segments to", text)
