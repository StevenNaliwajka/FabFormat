from abc import abstractmethod

from CodeBase.fileIO.CommonFormat.CFLayer.Additive.AdditiveTrace.Trace.cf_polygon_trace import CFPolygonTrace


class ApertureParent:
    def __init__(self):
        self.aperture_type = None
        self.aperture_number = None
        self.inner_hole_diameter = None
        self.common_form = []

    # Comparison function to make objects comparable based on aperture_number
    def __lt__(self, other):
        return self.aperture_number < other.aperture_number

    @abstractmethod
    def to_common_form(self, *args, **kwargs):
        pass

    def rectangle_to_cf(self, center_x, center_y, x_size, y_size):
        # Creates 1 CF polygon: EZ
        point_list = []
        # BL: BOTTOM LEFT
        # BR: BOTTOM RIGHT
        # TL: TOP LEFT
        # TR: TOP RIGHT
        # BL
        current_x = center_x - (x_size / 2)
        current_y = center_y - (y_size / 2)
        point_list.append(current_x)
        point_list.append(current_y)
        # TL
        current_y = current_y + y_size
        point_list.append(current_x)
        point_list.append(current_y)
        # TR
        current_x = current_x + x_size
        point_list.append(current_x)
        point_list.append(current_y)
        # BR
        current_y = current_y - y_size
        point_list.append(current_x)
        point_list.append(current_y)
        # BLx2
        current_x = current_x - x_size
        point_list.append(current_x)
        point_list.append(current_y)

        new_common_form = CFPolygonTrace(point_list)
        self.common_form.append(new_common_form)