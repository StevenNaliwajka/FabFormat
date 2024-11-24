import os

from CodeBase.fileIO.Output.OutputTypes.output_parent import OutputParent
from CodeBase.config.config import Config
from CodeBase.gui.gui import Gui

class WriteGcode(OutputParent):

    # CREATE METHOD TO GET LAYERS. AND HAVE IT CALL _verify_units_in_layer

    # USING https://marlinfw.org/docs/gcode/G000-G001.html AS A BIBLE
    def __init__(self, gcode_config, common_form):
        super().__init__(gcode_config.filepath, gcode_config.unit, common_form)
        self.config = None

        self.current_tool = "T0"  # T1 is the Conductive Material, T2 is Non-conductive.

    def write_headless(self, input_file_obj_list, config:Config, common_form):
        #
        # Gerber code output
        #
        # Bible: https://marlinfw.org/meta/gcode/
        # Iterate through common form.
        # For each layer:
        # plot the conductive traces first. on T0
        # Then plot the non-conductive trace. on T1
        # For now ignore detail traces.
        # Chat we are cooked.
        self.config = config
        self.out_file_path = os.path.join(self.config.output_path, self.config.outfile_name, ".gcode")

        self.write_file_header()
        self.write_file_settings_and_prime()


    def write_file_header(self):
        # Writes file header information
        with open(self.out_file_path, "w") as file:
            file.write(f"; G-CODE created on {self.config.date}\n"
                       f"; Flavor: Marlin\n"
                       f"; Generated using the FabFormat file converter.\n"
                       f"; https://github.com/StevenNaliwajka/FabFormat\n")

    def write_file_settings_and_prime(self):
        with open(self.out_file_path, "a") as file:
            # Set units G21
            # Set abs or relative positioning G90
            # home all axis G28
            # auto bed leveling G29 as toggle setting in config
            # set extruder temp
            # M104 T0 S200   set t0 = 200c
            # M104 T1 S140   set t1 = 140c
            # M140 S60       set bed temp to 60c
            # M190 S60       wait for bed temp to get to 60c
            # M109 T0 S200   wait for t0 to reach 200
            # M109 T1 S140   wait for t1 to reach 140

            # ; Prime each extruder individually
            # T0            ; Select extruder 1
            # G92 E0        ; Reset extruder position to zero
            # G1 Z0.2 F1200 ; Raise nozzle slightly
            # G1 X10 Y10 F3000 ; Move to the starting corner of the bed
            # G1 E10 F200   ; Extrude 10 mm of filament from extruder 1 to prime

            # T1            ; Switch to extruder 2
            # G92 E0        ; Reset extruder position to zero
            # G1 X20 Y10 F3000 ; Move slightly over to avoid mixing extruders
            # G1 E10 F200   ; Extrude 10 mm of filament from extruder 2 to prime

            # ; Move back to starting position with the first extruder selected
            # T0            ; Select extruder 1 to start the print
            # G1 X0 Y0 Z0.2 ; Move back to origin position

            # ; Start your print
            pass

    def write_gui(self, input_file_obj_list, GUI:Gui):
        #
        # G code output
        #
