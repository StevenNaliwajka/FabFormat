class CFTraceParent:

    def __init__(self, unit):
        # Parent for CF "Common Form" trace types.

        # What type it is "c","a","p","l"
        self._type = None
        self.unit = unit

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_value):
        if new_value in ("c", "a", "p", "l"):
            self._type = new_value
        else:
            raise ValueError("New Value is not a valid trace type.")