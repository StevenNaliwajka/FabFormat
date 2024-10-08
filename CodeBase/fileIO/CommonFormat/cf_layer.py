class CFLayer:

    def __init__(self, layer):
        # EXISTS TO STORE TRACE INFORMATION BY LAYER
        # CURRENTLY I THINK EVERY 'LINE' will have a different size.
        # CURRENTLY, EVERYTHING IS DIRECT AND NOT RELATIVE.
        self.layer = layer
        self.linear_trace_list = []
        self.arc_trace_list = []
        self.circle_trace_list = []

    def add_linear_trace(self, size, point_list):
        # Stores linear traces
        # Size of line, And the points that the line travels to in one stroke.
        self.linear_trace_list.append([size, point_list])

    def add_arc_trace(self, start, end, radius):
        # Stores start, end, radius data.
        self.arc_trace_list.append([start, end, radius])

    def add_circle_trace(self, radius, size, center):
        # Stores center, end, radius data
        self.circle_trace_list.append([radius, size, center])
