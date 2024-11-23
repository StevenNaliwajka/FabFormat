import numpy as np
import scipy.interpolate as si
import matplotlib.pyplot as plt
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.cf_shape_parent import CFShapeParent


class CFParametricCubicSplinePrim(CFShapeParent):
    # I'll roll my own solution to this after DEC 2nd to drop the scipy requirement.
    #  - Famous last words.

    def __init__(self, x_cord_list, y_cord_list, unit):
        super().__init__(unit)
        shared_value =
        self.type = "pcs"
        if len(x_cord_list) != len(y_cord_list):
            raise ValueError("x_cord_list and y_cord_list must have the same length.")

        self.x_cord_list = np.array(x_cord_list)
        self.y_cord_list = np.array(y_cord_list)

        # Calculate cumulative distances to use as 't' (parameter)
        distances = np.sqrt(np.diff(self.x_cord_list)**2 + np.diff(self.y_cord_list)**2)
        self.t = np.concatenate([[0], np.cumsum(distances)])

        # Normalize t to range [0, 1] for parametric control
        self.t_normalized = self.t / self.t[-1]

        # Fit cubic splines for x(t) and y(t)
        self.x_spline = si.CubicSpline(self.t_normalized, self.x_cord_list)
        self.y_spline = si.CubicSpline(self.t_normalized, self.y_cord_list)

        # This number is mutable. IDK what exact number to choose so ill go with 30 for now.
        t_qty = 30
        t_list = self._generate_sym_arc_t_values(t_qty)

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

    def _generate_sym_arc_t_values(self, quantity):
        """
        Generate evenly spaced values between 0 and 1 based on the quantity.

        :param quantity: Number of values to generate.
        :return: A list of values between 0 and 1.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        if quantity == 1:
            return [0]  # Special case: only one value at 0
        elif quantity == 2:
            return [0, 1]  # Special case: two values at 0 and 1

        # Generate evenly spaced values
        return [i / (quantity - 1) for i in range(quantity)]
