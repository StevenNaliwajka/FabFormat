from CodeBase.fileIO.CommonFormat.cf_layer import CFLayer


class AdditiveCF:

    def __init__(self):
        # EXISTS TO STORE CF DATA TO SIMPLIFY THINGS. ALLOWS FOR STANDARD FORMATING OF DATA

        # STORES LAYER OBJECTS.
        self.layer_data_list = []
        pass

    def add_layer(self):
        new_layer = CFLayer(len(self.layer_data_list))
        self.layer_data_list.append(new_layer)
