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
from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.intersection_operations.CF_CF_Additive_Handling import \
    cir_cir_additive_handling, cir_composite_additive_handling, cir_fsa_additive_handling, \
    composite_composite_additive_handling, fsa_composite_additive_handling, fsa_fsa_additive_handling
from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.intersection_operations.CF_CF_Intersection_test import \
    cir_cir_intersection, cir_fsa_intersection, cir_lin_intersection, cir_pcs_intersection, cir_sap_intersection, \
    fsa_fsa_intersection, fsa_lin_intersection, fsa_pcs_intersection, fsa_sap_intersection, lin_lin_intersection, \
    lin_sap_intersection, lin_pcs_intersection, pcs_pcs_intersection, pcs_sap_intersection, sap_sap_intersection
from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.intersection_operations.CF_CF_Subtractive_handling import \
    cir_cir_subtractive_handling, cir_composite_subtractive_handling, cir_fsa_subtractive_handling, \
    composite_composite_subtractive_handling, fsa_composite_subtractive_handling, fsa_fsa_subtractive_handling


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

        self.cf_shape_switcher = {
            # Shapes
            "cir": 2,  # Circle
            "fsa": 3,  # Filled_sym_arc
            # Primitives
            "lin": 5,  # Linear_prim
            "pcs": 7,  # Parametric_cub_spline_prim
            "sap": 11,  # symm_arc_prim
            # Composites
            "com": 13,  # complex shape (LIN,PCS,SAP)
            "pol": 17,  # Polygon (LIN only)
        }

        self.intersection_method_switcher = {
            # CF * CF = unique number.
            # CF number gotten from cf_shape_switcher above
            3: cir_cir_intersection,
            6: cir_fsa_intersection,
            10: cir_lin_intersection,
            14: cir_pcs_intersection,
            22: cir_sap_intersection,
            9: fsa_fsa_intersection,
            15: fsa_lin_intersection,
            21: fsa_pcs_intersection,
            33: fsa_sap_intersection,
            25: lin_lin_intersection,
            35: lin_pcs_intersection,
            55: lin_sap_intersection,
            49: pcs_pcs_intersection,
            77: pcs_sap_intersection,
            121: sap_sap_intersection,
        }

        self.additive_handling_switcher = {
            # CF * CF = unique number.
            # CF number gotten from cf_shape_switcher above
            4: cir_cir_additive_handling,
            26: cir_composite_additive_handling,  # COM
            34: cir_composite_additive_handling,  # POL
            6: cir_fsa_additive_handling,
            169: composite_composite_additive_handling,  # COM * COM
            221: composite_composite_additive_handling,  # COM * POL
            289: composite_composite_additive_handling,  # POL * POL
            39: fsa_composite_additive_handling,  # COM
            51: fsa_composite_additive_handling,  # POL
            9: fsa_fsa_additive_handling
        }

        self.subtractive_handling_switcher = {
            # CF * CF = unique number.
            # CF number gotten from cf_shape_switcher above
            4: cir_cir_subtractive_handling,
            26: cir_composite_subtractive_handling,  # COM
            34: cir_composite_subtractive_handling,  # POL
            6: cir_fsa_subtractive_handling,
            169: composite_composite_subtractive_handling,  # COM * COM
            221: composite_composite_subtractive_handling,  # COM * POL
            289: composite_composite_subtractive_handling,  # POL * POL
            39: fsa_composite_subtractive_handling,  # COM
            51: fsa_composite_subtractive_handling,  # POL
            9: fsa_fsa_subtractive_handling
        }

    # Composites
    def add_polygon(self, layer_list, type_of_trace, unit, primitive_list):
        # Creates new CF POLYGON obj, adds it to the correct list + layer
        new_trace = CFPolygon(unit, primitive_list)
        # VERIFY THAT ALL THE PRIMITIVES IN THE TRACE HAVE THE SAME UNIT. IF NOT CONVERT.
        self.add_trace_to_type(layer_list, type_of_trace, new_trace)

    def add_complex_shape(self, layer_list, type_of_trace, unit, primitive_list):
        # Creates new CF POLYGON obj, adds it to the correct list + layer
        new_trace = CFComplexShape(unit, primitive_list)
        # VERIFY THAT ALL THE PRIMITIVES IN THE TRACE HAVE THE SAME UNIT. IF NOT CONVERT.
        self.add_trace_to_type(layer_list, type_of_trace, new_trace)

    # Shapes
    def add_sym_arc(self, layer_list, type_of_trace, unit, center_pt, start_pt, end_pt, arc_radius, inner_off=None):
        # Creates new CF ARC obj, adds it to the correct list + layer
        #print(f"(CommonForm): Adding Symmetrical arc to layer: \"{layer_list}\", type: \"{type_of_trace}\".'.")
        new_trace = CFFilledSymmetricalArc(unit, center_pt, start_pt, end_pt, arc_radius, inner_off)
        self.add_trace_to_type(layer_list, type_of_trace, new_trace)

    def add_circle(self, layer_list, type_of_trace, unit, center_pt, radius, inner_radius=None):
        # Creates new CF CIRCLE obj, adds it to the correct list + layer
        new_trace = CFCircle(unit, center_pt, radius, inner_radius)
        self.add_trace_to_type(layer_list, type_of_trace, new_trace)

    def add_trace_to_type(self, layer_list, type_of_layer, trace_object):
        # Directly adds a trace object to a layer and layer type if the object has been created already.
        for layer in layer_list:
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
        new_trace = CFSymmetricalArcPrim(unit, center_pt, start_pt, end_pt, arc_radius)
        return new_trace

    def verify_units(self, outfile_config):
        for layer in self.layer_list:
            layer.verify_units(outfile_config)

    def format_layers(self):
        core_flag = 0
        depth_flag = 0
        annotation_flag = 0
        for config in self.output_config.outfile_list:
            if config.generate_core_bounded_by_outline:
                core_flag = 1
            if config.output_material_has_depth:
                depth_flag = 1
            if config.annotation_flag:
                annotation_flag = 1
        for layer in self.layer_list:
            if annotation_flag:
                # toggles annotations
                layer.set_annotation_flag()
            if depth_flag:
                # removes additive overlaps
                layer.remove_additive_overlaps()
            if core_flag:
                # generates core
                layer.generate_core()
            if depth_flag:
                # remove subtractive overlaps from additive.
                layer.remove_subtractive()
