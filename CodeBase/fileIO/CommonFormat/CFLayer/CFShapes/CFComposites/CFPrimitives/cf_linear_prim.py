from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_shape_parent import CFShapeParent


class CFLinearPrim(CFShapeParent):
    def __init__(self, unit, start_pt, end_pt):
        # SEE CurrentCFCheatSheat.PNG in
        # CHANGED. ONLY STORED AS A Line WITH ZERO SIZE. USED FOR BOUNDING WITH POLYGONS.

        super().__init__(unit)
        self.type = "lin"
        self.start_pt = start_pt
        self.end_pt = end_pt

    def _calculate_extreme_points(self):
        # By nature of linear, it's either the beginning or the end.
        # No need to calculate fancy stuff.
        self.extreme_points.append(self.start_pt)
        self.extreme_points.append(self.end_pt)

    def change_unit(self, new_unit):
        conversion_factor = None
        if new_unit == "mm":
            conversion_factor = 0.0393701
        else:
            conversion_factor = 25.4
        self.start_pt = tuple(element * conversion_factor for element in self.start_pt)
        self.end_pt = tuple(element * conversion_factor for element in self.end_pt)
        self.unit = new_unit

    def shift_cf(self, shift_x, shift_y):
        # Shift Start PT
        self.start_pt[0] = self.start_pt[0] + shift_x
        self.start_pt[1] = self.start_pt[1] + shift_y
        # Shift End PT
        self.end_pt[0] = self.end_pt[0] + shift_x
        self.end_pt[1] = self.end_pt[1] + shift_y

    def get_bounding_box(self):
        """
                Calculate and return the bounding box for the line.
                :return: A tuple containing (center_pt, width, height)
        """
        x1, y1 = self.start_pt
        x2, y2 = self.end_pt

        # Calculate the min and max x and y values
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        # Calculate the bounding box dimensions
        width = max_x - min_x
        height = max_y - min_y

        # Calculate the center point
        center_pt = ((min_x + max_x) / 2, (min_y + max_y) / 2)

        # Return the bounding box
        return center_pt, width, height