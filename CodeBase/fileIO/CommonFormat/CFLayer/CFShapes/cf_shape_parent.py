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

        # When finally finishing, calculated overlaping between CF can be done here.
        # STORED AS TOUPLE:
        # [(ID, pt_1, pt_2),....]
        # EX:
        # [(15,(0.5,3.4),(3.45,4.5)),(70,(3.4,4.5),(2.4,2.4)),...]
        # This CF intersects CF:15 between  (0.5,3.4) and (3.45,4.5)
        # It also intersects CF:70 between  (3.4,4.5) and (2.4,2.4)
        self.is_intersecting_other_shapes = []

        # After calculating overlaps, calculated touching between CF can be saved here.
        # STORED AS TOUPLE:
        # [(ID, pt_1, pt_2),....]
        # EX:
        # [(15,(0.5,3.4),(3.45,4.5)),(70,(3.4,4.5),(2.4,2.4)),...]
        # This CF touches CF:15 between  (0.5,3.4) and (3.45,4.5)
        # It also touches CF:70 between  (3.4,4.5) and (2.4,2.4)
        self.is_touching_other_shapes = []


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

    @abstractmethod
    def get_bounding_box(self):
        # gets bounding box and returns it.
        pass