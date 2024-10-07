class SubtractiveCF:

    def __init__(self):
        # EXISTS FOR NOW. NEED TO MOVE OVER EXELLON FILES.
        self.drill_tool_diameter = []
        self.holes = {}

    def new_tool(self, tool_number, tool_diameter):
        # Prevents error-ing of index out of rage by init-ing the drill_tool list to be of proper length.
        while len(self.drill_tool_diameter) <= tool_number - 1:
            self.drill_tool_diameter.append(None)

        # Drill tool #1 with a diameter of X,   is in drill_tool_diameter[0] with a value of X
        self.drill_tool_diameter[tool_number - 1] = tool_diameter

    def make_hole(self, drill_num, x_real, y_real):
        # Prevents error-ing of index out of rage by init-ing the drill_tool list to be of proper length.
        if drill_num not in self.holes:
            self.holes[drill_num] = []

        self.holes[drill_num].append([x_real, y_real])
