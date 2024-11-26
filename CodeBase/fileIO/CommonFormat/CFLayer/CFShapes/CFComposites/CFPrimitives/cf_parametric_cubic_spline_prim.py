import numpy as np
import scipy.interpolate as si
import matplotlib.pyplot as plt

from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_curve_parent import CFCurveParent


class CFParametricCubicSplinePrim(CFCurveParent):
    # I'll roll my own solution to this after DEC 2nd to drop the scipy requirement.
    #  - Famous last words.

    # This thing is a POS but, it's tested in isolation, and it works, Shift and update unit works.
    t_list = []

    def __init__(self, unit, x_cord_list, y_cord_list):
        qty_points_on_curve = 30
        super().__init__(unit, qty_points_on_curve)

        self.type = "pcs"
        self.list_of_outer_pts = []

        if len(x_cord_list) != len(y_cord_list):
            raise ValueError("x_cord_list and y_cord_list must have the same length.")

        self.x_cord_list = np.array(x_cord_list)
        self.y_cord_list = np.array(y_cord_list)

        # Calculate cumulative distances to use as 't' (parameter)
        distances = np.sqrt(np.diff(self.x_cord_list) ** 2 + np.diff(self.y_cord_list) ** 2)
        self.t = np.concatenate([[0], np.cumsum(distances)])

        # Normalize t to range [0, 1] for parametric control
        self.t_normalized = self.t / self.t[-1]
        # print(f"Normalized T: {self.t_normalized}")

        # Fit cubic splines for x(t) and y(t)
        self.x_spline = si.CubicSpline(self.t_normalized, self.x_cord_list)
        self.y_spline = si.CubicSpline(self.t_normalized, self.y_cord_list)

    def _calculate_points_on_curve(self):
        # print("Calculating points on curve")
        if not CFParametricCubicSplinePrim.t_list:
            self._generate_t_list()
        # print(f"TList: {CFParametricCubicSplinePrim.t_list}")
        for t in CFParametricCubicSplinePrim.t_list:
            # get the X,y for the equation
            gotten_pt = self.get_point(t)

            # Convert numpy arrays to native types
            x = float(gotten_pt[0]) if isinstance(gotten_pt[0], np.ndarray) else gotten_pt[0]
            y = float(gotten_pt[1]) if isinstance(gotten_pt[1], np.ndarray) else gotten_pt[1]

            # Append as a tuple of native Python numbers
            self.list_of_outer_pts.append((x, y))

    def _calculate_extreme_points(self):
        if not self.list_of_outer_pts:
            self._calculate_points_on_curve()
        self.extreme_points = self.list_of_outer_pts

    def get_points_on_curve(self):
        if not self.list_of_outer_pts:
            self._calculate_points_on_curve()
        return self.list_of_outer_pts

    def get_point(self, t_value):
        """
        Calculate the exact (x, y) point on the curve for a given parameter t_value.
        t_value must be in the range [0, 1].
        """
        if t_value < 0 or t_value > 1:
            raise ValueError("t_value must be in the range [0, 1].")

        x = self.x_spline(t_value)
        y = self.y_spline(t_value)
        return x, y

    def plot_curve(self, num_points=100):
        """
        Plot the parametric cubic spline.
        """
        t_values = np.linspace(0, 1, num_points)
        x_values = self.x_spline(t_values)
        y_values = self.y_spline(t_values)

        plt.figure(figsize=(8, 6))
        plt.plot(x_values, y_values, label="Parametric Cubic Spline")
        plt.scatter(self.x_cord_list, self.y_cord_list, color='red', label="Control Points")
        plt.title("Parametric Cubic Spline")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid()
        plt.show()

    def _generate_t_list(self):
        """
        Generate evenly spaced values between 0 and 1 based on the quantity.
        """
        if self.qty_point_on_curve <= 0:
            raise ValueError("Quantity must be a positive integer.")

        if self.qty_point_on_curve == 1:
            return [0]  # Special case: only one value at 0
        elif self.qty_point_on_curve == 2:
            return [0, 1]  # Special case: two values at 0 and 1

        # Generate evenly spaced values
        new_t_list = [i / (self.qty_point_on_curve - 1) for i in range(self.qty_point_on_curve)]
        CFParametricCubicSplinePrim.t_list = new_t_list
        # print(f"Current T-List: {CFParametricCubicSplinePrim.t_list}")

    def change_unit(self, new_unit):
        if new_unit == "mm":
            conversion_factor = 0.0393701  # inches to mm
        else:
            conversion_factor = 25.4  # mm to inches

        # Update coordinates
        self.x_cord_list = self.x_cord_list * conversion_factor
        self.y_cord_list = self.y_cord_list * conversion_factor

        # Recreate the splines
        self.x_spline = si.CubicSpline(self.t_normalized, self.x_cord_list)
        self.y_spline = si.CubicSpline(self.t_normalized, self.y_cord_list)

        # Clear cached points and recalculate
        self.list_of_outer_pts = []  # Clear previously calculated points
        self._calculate_points_on_curve()

        self.unit = new_unit

    def shift_cf(self, shift_x, shift_y):
        # Update coordinates by shifting
        self.x_cord_list = self.x_cord_list + shift_x
        self.y_cord_list = self.y_cord_list + shift_y

        # Recreate the splines
        self.x_spline = si.CubicSpline(self.t_normalized, self.x_cord_list)
        self.y_spline = si.CubicSpline(self.t_normalized, self.y_cord_list)

        # Clear cached points and recalculate
        self.list_of_outer_pts = []  # Clear previously calculated points
        self._calculate_points_on_curve()

    def get_bounding_box(self):
        """
        Calculates the bounding box for a curved line given a list of points.

        Parameters:
            points (list of tuple): List of (x, y) tuples representing the points of the curved line.

        Returns:
            tuple: A tuple containing:
                - center_pt (tuple): Center point of the bounding box as (x, y).
                - width (float): Width of the bounding box.
                - height (float): Height of the bounding box.
        """
        if not self.list_of_outer_pts or len(self.list_of_outer_pts) < 2:
            raise ValueError("At least two self.list_of_outer_pts are required to calculate a bounding box.")

        # Extract x and y coordinates
        x_coords = [pt[0] for pt in self.list_of_outer_pts]
        y_coords = [pt[1] for pt in self.list_of_outer_pts]

        # Calculate min and max for x and y
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        # Calculate the width and height of the bounding box
        width = x_max - x_min
        height = y_max - y_min

        # Calculate the center point of the bounding box
        center_pt = ((x_min + x_max) / 2, (y_min + y_max) / 2)

        # Return the bounding box as a tuple
        return center_pt, width, height