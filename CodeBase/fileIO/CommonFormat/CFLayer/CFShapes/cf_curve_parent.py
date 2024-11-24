import math
from abc import abstractmethod

from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_shape_parent import CFShapeParent


class CFCurveParent(CFShapeParent):
    def __init__(self, unit, qty_points_on_curve):
        # Parent for CF "Common Form" trace types.

        # What type it is "c","a","p","l"
        super().__init__(unit)
        self.qty_point_on_curve = qty_points_on_curve
        self.list_of_outer_pts = []

    @abstractmethod
    def _calculate_points_on_curve(self):
        pass

    def _generate_circular_points(self, center, radius, start_point=None, degree_step=None):
        list_of_new_pts = []
        if start_point and degree_step:
            # Method 1: Start at a fixed point and add points in a clockwise direction
            start_angle = math.atan2(start_point[1] - center[1], start_point[0] - center[0])
            for i in range(self.qty_point_on_curve):
                angle = start_angle + math.radians(degree_step) * i
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                list_of_new_pts.append((x, y))
        elif self.qty_point_on_curve:
            # Method 2: Cover the whole circle with evenly spaced points
            for i in range(self.qty_point_on_curve):
                angle = 2 * math.pi * i / self.qty_point_on_curve
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                list_of_new_pts.append((x, y))
        else:
            raise ValueError("Specify either a start_point and degree_step or num_points.")
        return list_of_new_pts
