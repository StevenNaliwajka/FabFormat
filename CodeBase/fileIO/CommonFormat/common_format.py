class CommonFormat:

    def __init__(self, cf_type):
        # EXISTS TO STORE CF DATA TO SIMPLIFY THINGS. ALLOWS FOR STANDARD FORMATING OF DATA
        # IS EITHER ADDITIVE OR SUBTRACTIVE.
        if cf_type == "additive":
            # STORES LAYER OBJECTS.
            self.layer_data_list = []
            pass
        if cf_type == "subtractive":
            # EXISTS FOR NOW. NEED TO MOVE OVER EXELLON FILES.
            self.drill_tool_diameter = []
            self.holes = {}
            pass