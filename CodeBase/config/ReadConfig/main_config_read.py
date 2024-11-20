from CodeBase.config.ConfigFiles.gui_config import GUIConfig
from CodeBase.config.ConfigFiles.infile_config import InfileConfig
from CodeBase.config.ConfigFiles.outfile_config import OutfileConfig
from CodeBase.config.ReadConfig.ReadConfigMethods.read_gui_config import read_gui_config
from CodeBase.config.ReadConfig.ReadConfigMethods.read_input_config import read_input_config
from CodeBase.config.ReadConfig.ReadConfigMethods.read_output_config import read_output_config


def main_config_read(infile_directory_path):
    gui_config = None
    # Create infile_config
    infile_config = InfileConfig(infile_directory_path)

    # read input_config
    read_input_config(infile_config)

    # if gui on, read it.
    if infile_config.gui_state:
        gui_config = GUIConfig()
        read_gui_config(gui_config)

    # Create outfile_config
    outfile_config = OutfileConfig(infile_config.outfile_directory_path)

    # read output config
    read_output_config(outfile_config)

    # send back
    return gui_config, infile_config, outfile_config
