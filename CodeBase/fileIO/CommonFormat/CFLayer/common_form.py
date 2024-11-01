from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.curves.cf_arc_trace import CFArcTrace
from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_linear_trace import CFLinearTrace
from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.CommonFormat.CFLayer.Additive.additive_layer import AdditiveLayer


class CommonForm:
    def __init__(self):
        # STORES CF(CommonForm) data
        # 1 Instance per outfile.

        # Layer List, creates and stores a 'additive_layer_cf' obj and inputs it into the correct pos in list,
        # "additive_layer_cf" then stores all the trace info for that layer.
        # [0] = layer 1
        # [1] = Layer 2
        self.conductive_trace_by_layer = []
        # same as above, but stores detail traces not conductive traces. 3RD Material
        self.detail_trace_by_layer = []
        # same as above, stores outline traces for boundary of board.
        # In theory supports an outline per layer. Allowing custom geometry
        self.outline_trace_by_layer = []

        ##NOOOOOTTTT RIGHT RNNN. NEED TO FIX TO MATCH ADDITIVE STANDARD
        # Vias, Throughholes
        # [0], instructins for Tool 1,
        # [1] instructions for tool 2,
        # etc....
        self.holes = []
        # [0], Defiles info for tool 1, Area
        self.holes_toolinfo = []

    def add_arc(self, layer, type_of_layer, size_of_line, start_x_y, end_x_y, radius):
        # Creates new CF ARC obj, adds it to the correct list + layer
        new_trace = CFArcTrace(size_of_line, start_x_y, end_x_y, radius)
        self.add_trace_to_type(layer, type_of_layer, new_trace)

    def add_circle(self, layer, type_of_layer, size_of_line, radius, center_x_y, infill, omitted_hole=None):
        # Creates new CF CIRCLE obj, adds it to the correct list + layer
        new_trace = CFCircleTrace(size_of_line, radius, center_x_y, infill, omitted_hole)
        self.add_trace_to_type(layer, type_of_layer, new_trace)

    def add_linear(self, layer, type_of_layer, size_of_line, start_x_y, end_x_y):
        # Creates new CF LINEAR obj, adds it to the correct list + layer
        new_trace = CFLinearTrace(size_of_line, start_x_y, end_x_y)
        self.add_trace_to_type(layer, type_of_layer, new_trace)

    def add_polygon(self, layer, type_of_layer, point_list, infill=0, omitted_hole=None):
        # Creates new CF POLYGON obj, adds it to the correct list + layer
        new_trace = CFPolygonTrace(point_list, infill, omitted_hole)
        self.add_trace_to_type(layer, type_of_layer, new_trace)

    def add_trace_to_type(self, layer, type_of_layer, trace_object):
        # Adds created trace to the correct category of list.
        if type_of_layer == "conductive":
            self.add_trace_to_layer(self.conductive_trace_by_layer, layer, trace_object)
        elif type_of_layer == "detail":
            self.add_trace_to_layer(self.detail_trace_by_layer, layer, trace_object)
        elif type_of_layer == "outline":
            self.add_trace_to_layer(self.outline_trace_by_layer, layer, trace_object)
        else:
            raise ValueError(f"COMMON FORM: \"{type_of_layer}\" is not an acceptable trace category.")

    def add_trace_to_layer(self, layer_list_to_append, layer, trace_object):
        # Adds trace to the correct layer in the specified category of list.
        target_list = getattr(self, layer_list_to_append)
        if len(target_list) < layer:
            target_list.extend([None] * (layer - len(layer)))
        if target_list[layer - 1] is None:
            target_list[layer - 1] = AdditiveLayer(layer)
        target_list[layer - 1].addtrace(trace_object)
