import copy

from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.cf_handle_intersection import \
    cf_handle_intersection
from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.cf_map_shapes import cf_map_shapes

from CodeBase.fileIO.CommonFormat.CFOperations.CFIntersectionHandler.intersection_operations.check_for_cf_intersection import \
    check_for_cf_intersection
from CodeBase.fileIO.CommonFormat.CFOperations.cf_generate_core_traces import cf_generate_core_traces


class CFTraceLayer:
    def __init__(self, layer_number, common_format):
        # Stores CF data for A layer
        self.layer_numer = layer_number
        self.common_format = common_format

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

        # flags whether annotations are cared about
        self.annotation_traces_flag = 0
        # flags whether map shapes has run yet. O till not
        self.map_shapes_flag = 0
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
        self.map_shapes_flag = 1
        # calls a method to map the shapes relations with each other, whats overlaping, whats touching etc....
        # passes in a certain layer.
        cf_map_shapes(self.primary_traces)
        cf_map_shapes(self.annotation_traces)

    def generate_core(self):
        # generates core thats bounded by outline
        # generates core everywhere thats not primary, subtractive, or annotation if boolean
        if self.map_shapes_flag:
            self.map_shapes()
        self.core_traces = cf_generate_core_traces(self.primary_traces, self.subtractive_traces, self.annotation_traces)
        # Generates core traces.

    def remove_subtractive(self):
        # Removes subtractive traces from primary.
        '''
        if self.map_shapes_flag:
            self.map_shapes()
        '''

        subtractive_method_switcher = {

        }

        # Copy primary_traces to modified_primary_traces to begin modifying
        self.modified_primary_traces = self.primary_traces.copy()

        # for every new subtractive trace
        for subtractive_trace in self.subtractive_traces:
            # itterate through the updated modified_primary_traces
            for index, trace in enumerate(self.modified_primary_traces):
                # Get intersection data
                intersection = check_for_cf_intersection(trace, subtractive_trace, self.common_format)
                # IF no intersection it returns None. Else
                if intersection:
                    # handle the intersection
                    modified_traces = cf_handle_intersection(False, intersection, self.common_format)

                    # if the returned traces are NOTHING
                    if modified_traces is None:
                        # do nothing
                        pass
                    else:
                        # Remove OG trace
                        del self.modified_primary_traces[index]
                        # Copy the modified traces over to the modified_primary_traces.
                        self.modified_primary_traces.extend(modified_traces)

    def remove_additive_overlaps(self):
        # Removes subtractive traces from primary.
        '''
        if self.map_shapes_flag:
            self.map_shapes()
        '''

        index_in_list = 0
        while index_in_list < len(self.primary_traces):
            check_cf = self.primary_traces[index_in_list]
            for index, trace in enumerate(self.primary_traces):
                # Get intersection data
                intersection = check_for_cf_intersection(trace, check_cf, self.common_format)
                # IF no intersection it returns None and goes to the next object. Else handles intersection
                if intersection:
                    # handle the intersection
                    modified_traces = cf_handle_intersection(True, intersection, self.common_format)

                    # Remove OG trace
                    del self.modified_primary_traces[index]
                    # Copy the modified traces over to the modified_primary_traces.
                    self.modified_primary_traces.extend(modified_traces)
                else:
                    # Since no intersection. go to next line
                    index_in_list += 1

    def set_annotation_flag(self):
        self.annotation_traces_flag = 1
