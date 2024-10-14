class CFTraceParent:

    def __init__(self):
        # Parent for CF "Common Form" trace types.

        # What type it is "c","a","p","l"
        self._type = None
        # Size of trace
        self.size_of_line = None
        self.point_list = []

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_value):
        if new_value in ("c", "a", "p", "l"):
            self._type = new_value
        else:
            raise ValueError("New Value is not a valid trace type.")