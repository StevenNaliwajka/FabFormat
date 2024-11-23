import math


class CFShapeParent:

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
        self._type = new_value

    def _calculate_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)