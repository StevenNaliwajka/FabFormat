
class CommonForm:
    def __init__(self):
        # STORES CF(CommonForm) data
        # 1 Instance per outfile.

        # Layer List, creates and stores a 'conductive_layer_cf' obj and inputs it into the correct pos in list,
        # "conductive_layer_cf" then stores all the trace info for that layer.
        # [0] = layer 1
        # [1] = Layer 2
        self.conductive_trace_by_layer = []
        # stores one trace that acts as the outer boarder. If non-existing interpreted as (min-max of traces) * margin
        ## Future is to implement outlines for each layer for unique form factors. NOT RN, Algo would be a SOB to do.
        self.outline = None
        # Vias, Throughholes
        # [0], instructins for Tool 1,
        # [1] instructions for tool 2,
        # etc....
        self.holes = []
        # [0], Defiles info for tool 1, Area
        self.holes_toolinfo = []

        ## IF 3 FILLAMENT PRINTING CAN BE LEVERAGED, DETAILING CAN BE PRITNED INTO THE BOARD.
        # NOT PART OF SCOPE. NO ACCESS TO 3 FILLAMENT PRINTER ANYWAYS.

    def add_conductive_traces(self, trace, layer):
        self.conductive_trace_by_layer[layer]