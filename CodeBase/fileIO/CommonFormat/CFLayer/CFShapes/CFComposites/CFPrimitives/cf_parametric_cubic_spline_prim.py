import numpy as np
import scipy.interpolate as si
import matplotlib.pyplot as plt

from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_curve_parent import CFCurveParent


class CFParametricCubicSplinePrim(CFCurveParent):
    # I'll roll my own solution to this after DEC 2nd to drop the scipy requirement.
    #  - Famous last words.

    def __init__(self, unit, x_cord_list, y_cord_list):
        qty_points_on_curve = 30
        super().__init__(unit, qty_points_on_curve)
        self.type = "pcs"

        if len(x_cord_list) != len(y_cord_list):
            raise ValueError("x_cord_list and y_cord_list must have the same length.")

        self.x_cord_list = np.array(x_cord_list)
        self.y_cord_list = np.array(y_cord_list)

        # Calculate cumulative distances to use as 't' (parameter)
        distances = np.sqrt(np.diff(self.x_cord_list) ** 2 + np.diff(self.y_cord_list) ** 2)
        self.t = np.concatenate([[0], np.cumsum(distances)])

        # Normalize t to range [0, 1] for parametric control
        self.t_normalized = self.t / self.t[-1]

        # Fit cubic splines for x(t) and y(t)
        self.x_spline = si.CubicSpline(self.t_normalized, self.x_cord_list)
        self.y_spline = si.CubicSpline(self.t_normalized, self.y_cord_list)

        self.t_list = []

    def _calculate_points_on_curve(self):
        # for every point generated
        for t in self.t_list:
            # get the X,y for the equation
            gotten_pt = self.get_point(t)
            # Check further
            self.list_of_outer_pts.append(gotten_pt)

    def _calculate_extreme_points(self):
        if self.list_of_outer_pts is None:
            self._calculate_points_on_curve()
        self.extreme_points = self.list_of_outer_pts

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

        :param quantity: Number of values to generate.
        :return: A list of values between 0 and 1.
        """
        if self.qty_point_on_curve <= 0:
            raise ValueError("Quantity must be a positive integer.")

        if self.qty_point_on_curve == 1:
            return [0]  # Special case: only one value at 0
        elif self.qty_point_on_curve == 2:
            return [0, 1]  # Special case: two values at 0 and 1

        # Generate evenly spaced values
        return [i / (self.qty_point_on_curve - 1) for i in range(self.qty_point_on_curve)]

    def change_unit(self, new_unit):
        conversion_factor = None
        if new_unit == "mm":
            conversion_factor = 0.0393701
        else:
            conversion_factor: 25.4
        self.x_cord_list = tuple(element * conversion_factor for element in self.x_cord_list)
        self.y_cord_list = tuple(element * conversion_factor for element in self.y_cord_list)
        self.x_spline = si.CubicSpline(self.x_spline.x, self.x_spline.c * conversion_factor, extrapolate=True)
        self.y_spline = si.CubicSpline(self.y_spline.x, self.y_spline.c * conversion_factor, extrapolate=True)
        self.list_of_outer_pts = tuple(element * conversion_factor for element in self.list_of_outer_pts)
        self.unit = new_unit