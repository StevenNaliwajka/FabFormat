from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFComposites.cf_complex_shape import CFComplexShape
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFComposites.cf_polygon import CFPolygon
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFPrimitives.cf_linear_prim import CFLinearPrim
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFPrimitives.cf_parametric_cubic_spline_prim import \
    CFParametricCubicSplinePrim
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFComposites.CFPrimitives.cf_symmetrical_arc_prim import \
    CFSymmetricalArcPrim
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_circle import CFCircle
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_filled_symmetrical_arc import CFFilledSymmetricalArc
from CodeBase.fileIO.CommonFormat.CFLayer.cf_layer import CFTraceLayer


class CommonForm:
    def __init__(self, input_config, output_config):
        # STORES CF(CommonForm) data
        # 1 Instance per creation.

        # Stores Layer objects from cf_layer.py
        # [0], layer 1.
        # [1], layer 2.
        # etc...
        self.layer_list = []
        self.input_config = input_config
        self.output_config = output_config

    # Composites
    def add_polygon(self, layer_num, type_of_trace, unit, primitive_list):
        # Creates new CF POLYGON obj, adds it to the correct list + layer
        new_trace = CFPolygon(unit, primitive_list)
        # VERIFY THAT ALL THE PRIMITIVES IN THE TRACE HAVE THE SAME UNIT. IF NOT CONVERT.
        self.add_trace_to_type(layer_num, type_of_trace, new_trace)

    def add_complex_shape(self, layer_num, type_of_trace, unit, primitive_list):
        # Creates new CF POLYGON obj, adds it to the correct list + layer
        new_trace = CFComplexShape(unit, primitive_list)
        # VERIFY THAT ALL THE PRIMITIVES IN THE TRACE HAVE THE SAME UNIT. IF NOT CONVERT.
        self.add_trace_to_type(layer_num, type_of_trace, new_trace)

    # Shapes
    def add_sym_arc(self, layer_num, type_of_trace, unit, center_pt, start_pt, end_pt, arc_radius, inner_off=None):
        # Creates new CF ARC obj, adds it to the correct list + layer
        #print(f"(CommonForm): Adding Symmetrical arc to layer: \"{layer_num}\", type: \"{type_of_trace}\".'.")
        new_trace = CFFilledSymmetricalArc(unit, center_pt, start_pt, end_pt, arc_radius, inner_off)
        self.add_trace_to_type(layer_num, type_of_trace, new_trace)

    def add_circle(self, layer_num, type_of_trace, unit, center_pt, radius, inner_radius=None):
        # Creates new CF CIRCLE obj, adds it to the correct list + layer
        new_trace = CFCircle(unit, center_pt, radius, inner_radius)
        self.add_trace_to_type(layer_num, type_of_trace, new_trace)

    def add_trace_to_type(self, layer, type_of_layer, trace_object):
        # Directly adds a trace object to a layer and layer type if the object has been created already.

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

    # Primitives
    def create_linear_prim(self, unit, start_pt, end_pt):
        # Creates new CF LINEAR obj, adds it to the correct list + layer
        new_trace = CFLinearPrim(unit, start_pt, end_pt)
        return new_trace

    def create_parametric_cubic_spline(self, unit, x_cord_list, y_cord_list):
        # Creates new CF Parametric cubic spline obj, adds it to the correct list + layer
        new_trace = CFParametricCubicSplinePrim(x_cord_list, y_cord_list, unit)
        return new_trace

    def add_sym_arc_prim(self, unit, center_pt, start_pt, end_pt, arc_radius):
        # Creates new CF ARC obj, adds it to the correct list + layer
        #print(f"(CommonForm): Adding Symmetrical arc to layer: \"{layer_num}\", type: \"{type_of_trace}\".'.")
        new_trace = CFSymmetricalArcPrim(unit, center_pt, start_pt, end_pt, arc_radius)
        return new_trace

    def verify_units(self, outfile_config):
        for layer in self.layer_list:
            layer.verify_units(outfile_config)

    def format_layers(self):
        pass
