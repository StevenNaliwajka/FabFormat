from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_linear_trace import CFLinearTrace


class AdditiveLayer:
    def __init__(self, layer_number):
        # EXISTS TO STORE DATA FOR TRACES OR DETAILS.
        # MAKE SEPERATE OBJ FOR TRACES + DETAILS.
        self.layer_number = layer_number

        # STORES TRACE INFO
        self.linear_trace_list = []
        self.arc_trace_list = []
        self.circle_trace_list = []
        self.polygon_trace_list = []

    ## TBD: BE SMART IN ADDING TRACES, MAYBE CONSIDER ADDING THEM IN ORDER SOMEHOW.... NOT MY PROBLEM RN LMAO.
    def add_trace(self, trace):
        if trace.type == "a":
            self.arc_trace_list.append(trace)
        elif trace.type == "c":
            self.circle_trace_list.append(trace)
        elif trace.type == "l":
            self.linear_trace_list.append(trace)
        elif trace.type == "p":
            self.polygon_trace_list.append(trace)
        else:
            raise ValueError(f"ADDITIVE LAYER: Invalid Trace type \"{trace.type}\".")
