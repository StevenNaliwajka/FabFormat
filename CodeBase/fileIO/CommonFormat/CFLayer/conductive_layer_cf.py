from CodeBase.fileIO.CommonFormat.CFLayer.TraceInfo.cf_layer import CFLayer


class AdditiveCF:

    def __init__(self):
        # EXISTS TO STORE CF DATA TO SIMPLIFY THINGS. ALLOWS FOR STANDARD FORMATING OF DATA
        # TO BE IMPLEMENTED... #STORE DATA IN FORMAT OF OUTPUT FILE*******************************************
        # STORES LAYER OBJECTS.
        self.layer_data_list = []
        pass

    def add_layer(self):
        # Creates a new Common Form Layer and adds it to the list
        # ASSUMES STARTING WITH LAYER 0 then 1... etc
        new_layer = CFLayer(len(self.layer_data_list))
        self.layer_data_list.append(new_layer)
