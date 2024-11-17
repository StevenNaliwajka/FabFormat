from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.cf_linear_trace import CFLinearTrace
from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.cf_polygon_trace import CFPolygonTrace
from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_circle_trace import CFCircleTrace
from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.curves.cf_symmetrical_arc_trace import CFSymmetricalArcTrace
from CodeBase.fileIO.CommonFormat.CFLayer.cf_layer import CFTraceLayer


class CommonForm:
    def __init__(self):
        # STORES CF(CommonForm) data
        # 1 Instance per creation.

        # Stores Layer objects from cf_layer.py
        # [0], layer 1.
        # [1], layer 2.
        # etc...
        self.layer_list = []

    def add_arc(self, layer_num, type_of_trace, c_x, c_y, s_x, s_y, e_x, e_y, radius, inner_off):
        # Creates new CF ARC obj, adds it to the correct list + layer
        #print(f"(CommonForm): Adding Symmetrical arc to layer: \"{layer_num}\", type: \"{type_of_trace}\".'.")
        new_trace = CFSymmetricalArcTrace(c_x, c_y, s_x, s_y, e_x, e_y, radius, inner_off)
        self.add_trace_to_type(layer_num, type_of_trace, new_trace)

    def add_circle(self, layer_num, type_of_trace, center_x, center_y, radius, inner_radius=None):
        # Creates new CF CIRCLE obj, adds it to the correct list + layer
        new_trace = CFCircleTrace(center_x, center_y, radius, inner_radius)
        self.add_trace_to_type(layer_num, type_of_trace, new_trace)

    def add_linear(self, layer_num, type_of_trace, start_x, start_y, end_x, end_y, size_of_line):
        # Creates new CF LINEAR obj, adds it to the correct list + layer
        new_trace = CFLinearTrace(start_x, start_y, end_x, end_y, size_of_line)
        self.add_trace_to_type(layer_num, type_of_trace, new_trace)

    def add_polygon(self, layer_num, type_of_trace, point_list):
        # Creates new CF POLYGON obj, adds it to the correct list + layer
        new_trace = CFPolygonTrace(point_list)
        self.add_trace_to_type(layer_num, type_of_trace, new_trace)

    def add_trace_to_type(self, layer, type_of_layer, trace_object):
        # Checks if layer exists
        if layer <= len(self.layer_list):
            # adds trace to layer
            pass
        else:
            # creates layer
            new_layer = CFTraceLayer(layer)
            self.layer_list.append(new_layer)
        # adds trace to layer
        self.layer_list[layer].add_trace_to_layer(type_of_layer, trace_object)

