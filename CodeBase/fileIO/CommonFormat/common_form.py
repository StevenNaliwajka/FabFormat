
class CommonForm:
    def __init__(self):
        #STORES CF(CommonForm) data
        # 1 Instance per outfile.

        # Layer List, creates and stores a layer obj
        # [0] = layer 1, etc...
        self.conductive_trace_by_layer = []
        self.outline = None
        self.vias = []

    def add_conductive_traces(self, trace, layer):
        self.conductive_trace_by_layer[layer]