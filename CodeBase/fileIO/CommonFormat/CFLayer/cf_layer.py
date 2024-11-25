class CFTraceLayer:
    def __init__(self, layer_number):
        # Stores CF data for A layer
        self.layer_numer = layer_number

        # raw primary_trace_data
        # primary_traces tend to be the unique material or goal.
        # Conductive Filament traces or the cut line for a CNC machine are examples.
        self.primary_traces = []

        # modified primary_trace_data
        # primary trace data that has been removed by subtractive_trace ends up here.
        self.modified_primary_traces = []

        # Subtractive_traces contain the traces that make up through_holes.
        self.subtractive_traces = []

        # Exclusive Subtractive Traces only prevent core_traces from being created in an additive setting.
        # In subtractive setting they are lumped in with primary traces
        # IF EXCLUSIVE SUBTRACTIVE TRACES INTERSECT WITH A PRIMARY TRACE, CONSIDERED A VIA. CARRIED BETWEEN LEVELS.
        self.exclusive_traces = []

        # Detail_Traces contain labels, names, numbers.
        # a 3rd color that will not typically show up in 3D Printing.
        # mainly shows in .jpg
        self.annotation_traces = []

        # Outline_Traces define the outer and inner edge of the creation.
        # Only Polylines/Circles allowed.
        self.outline_traces = []

        # Innert_Traces Define the innert part of the creation.
        # Tends to only be used in additive manufacturing to define a 2nd innert material.
        self.core_traces = []

        # SEE FLOW CHART FOR HOW CF WORKS

    def add_trace_to_layer(self, trace_type, trace):
        if trace_type.lower() in {"p", "primary", "primary_trace"}:
            self.primary_traces.append(trace)
        elif trace_type.lower() in {"m", "modified", "modified_primary_trace"}:
            self.modified_primary_traces.append(trace)
        elif trace_type.lower() in {"s", "subtractive", "subtractive_trace"}:
            self.subtractive_traces.append(trace)
        elif trace_type.lower() in {"a", "annotation", "annotation_trace"}:
            self.annotation_traces.append(trace)
        elif trace_type.lower() in {"o", "outline", "outline_trace"}:
            self.outline_traces.append(trace)
        elif trace_type.lower() in {"c", "core", "core_trace"}:
            self.core_traces.append(trace)
        elif trace_type.lower() in {"e", "exclusive", "exclusive_trace"}:
            self.exclusive_traces.append(trace)
        else:
            raise ValueError(f"ADDITIVE LAYER: Invalid Trace type \"{trace_type}\".")

    def map_shapes(self):
        # calls a method to map the shapes relations with each other, whats overlaping, whats touching etc....
        # passes in a certain layer.