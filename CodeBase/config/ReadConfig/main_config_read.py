from CodeBase.config.ConfigFiles.Files.InfileConfig.infile_config import InfileConfig
from CodeBase.config.ConfigFiles.Files.OutfileConfig.outfile_config import OutfileConfig
from CodeBase.config.ConfigFiles.GUI.gui_config import GUIConfig
from CodeBase.config.ReadConfig.configs.read_gui_config import read_gui_config
from CodeBase.config.ReadConfig.configs.read_input_config import read_input_config
from CodeBase.config.ReadConfig.configs.read_output_config import read_output_config


def main_config_read(infile_directory_path, outfile_directory_path):
    gui_config = None
    infile_config = InfileConfig(infile_directory_path)
    outfile_config = OutfileConfig(outfile_directory_path)

    # readinput config
    read_input_config(infile_config)

    # if gui on, read it.
    if infile_config.gui_state:
        gui_config = GUIConfig()
        read_gui_config(gui_config)

    # read output config
    read_output_config(outfile_config)

    # send back
    return gui_config, infile_config, outfile_config
