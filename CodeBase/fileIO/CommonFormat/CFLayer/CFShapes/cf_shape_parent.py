import math
from abc import abstractmethod


class CFShapeParent:
    _id_counter = 1
    def __init__(self, unit):
        # Parent for CF "Common Form" trace types.

        # What type it is "c","a","p","l"
        self._type = None
        self.unit = unit
        self.extreme_points = []
        self.id = CFShapeParent._id_counter

        CFShapeParent._id_counter+=1

    def get_extreme_points(self):
        if self.extreme_points is None:
            # "if empty calculate"
            self._calculate_extreme_points()
        return self.extreme_points

    @abstractmethod
    def shift_cf(self, shift_x, shift_y):
        pass

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_value):
        self._type = new_value

    @abstractmethod
    def _calculate_extreme_points(self):
        # "calculates extreme pts"
        pass

    @abstractmethod
    def change_unit(self, new_unit):
        pass
