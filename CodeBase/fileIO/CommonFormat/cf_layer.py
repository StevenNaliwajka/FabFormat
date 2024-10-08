class CFLayer:

    def __init__(self, layer):
        # EXISTS TO STORE TRACE INFORMATION BY LAYER
        # CURRENTLY I THINK EVERY 'LINE' will have a different size.
        # CURRENTLY, EVERYTHING IS DIRECT AND NOT RELATIVE.
        self.layer = layer
        self.linear_trace_list = []
        self.arc_trace_list = []
        self.circle_trace_list = []

        ## NEED TO IMPLEMENT CONDITIONAL INFIL OF POLYGONS/CIRCLES
        ## INFIL FLAG SIGNALS OUTIFLE PARSER TO PROCEDURALY FILL THE SPACE OR NOT ACCORDING TO INFIL?

        ## I THINK I CAN SWAP FROM STORING SIZE OF LINE TO STORING A SEPERATE TOOL LIST
        ## SIMILAR TO HOW SUBTRACTIVE CF STORES THAT INFO.
        ## PASS TRACE INFO [TOOL][SHAPE][XY/CORDINFO][IF:C/P INFIL?]
        ## PASS TOOL INFO [SIZE]

        ## CONSIDER READING OUTFILE'S OUTPUT FORMAT METRIC/IN AND HAVING COMMON FORMAT'S
        ## STANDARD THE OUTFILE FORMAT.
        ## THIS OR HAVE UNIVERSAL METRIC

        ## NEED TO UPDATE THE CAPS INFORMATION TO ASSUME CAPS.. THEN IF IT DOES NOT FIND.
        ## RE-LOOP WITH A .toLower()

    def add_single_linear_trace(self, size, point_list):
        # Stores linear traces
        # Size of line, And the points that the line travels to in one stroke.
        self.linear_trace_list.append([size, point_list])

    def add_polygon_trace(self, size, point_list):
        # Stores linear traces
        # Size of line, And the points that the line travels to in a stroke.
        ## MUST RETURN TO OG POINT. ADD ERROR CHECKING.
        self.linear_trace_list.append([size, point_list])

    def add_arc_trace(self, start, end, radius):
        # Stores start, end, radius data.
        self.arc_trace_list.append([start, end, radius])

    def add_circle_trace(self, radius, size, center):
        # Stores center, end, radius data
        self.circle_trace_list.append([radius, size, center])
