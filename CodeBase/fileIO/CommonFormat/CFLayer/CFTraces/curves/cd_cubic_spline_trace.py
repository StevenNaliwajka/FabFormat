from CodeBase.fileIO.CommonFormat.CFLayer.CFTraces.cf_complex_parent import CFComplexParent


class CFCublicSplineTrace(CFComplexParent):
    def __init__(self, unit, x_cord_list, y_cord_List):
        super().__init__(unit)
        coefficients = self.cubic_spline(x_cord_list, y_cord_List)
        # List of X points on curve
        self.x_cord_list = self.generate_points(x_cord_list, num_points=100)
        # List of Y points on curve
        self.y_cord_list = self.evaluate_spline(x_cord_list, coefficients, self.x_cord_list)

    def evaluate_spline(self, x_cord_list, coefficients, x_points):
        """
        Evaluate the cubic spline at given x_points.
        Args:
            x_cord_list (list): Original x-coordinates.
            coefficients (list): Coefficients [(a, b, c, d), ...].
            x_points (list): Points to evaluate the spline at.
        Returns:
            List of evaluated y-coordinates.
        """
        y_points = []
        for xp in x_points:
            for i in range(len(x_cord_list) - 1):
                if x_cord_list[i] <= xp <= x_cord_list[i + 1]:
                    a, b, c, d = coefficients[i]
                    dx = xp - x_cord_list[i]
                    y_points.append(a + b * dx + c * dx ** 2 + d * dx ** 3)
                    break
        return y_points

    def cubic_spline(self, x, y):
        """
        Compute cubic spline coefficients for given points.
        Args:
            x (list): x-coordinates of points.
            y (list): y-coordinates of points.
        Returns:
            List of coefficients [(a, b, c, d), ...] for each interval.
        """
        n = len(x) - 1  # Number of intervals
        h = [x[i + 1] - x[i] for i in range(n)]  # Step sizes

        # Step 1: Set up the tridiagonal system
        alpha = [0] * (n + 1)  # Right-hand side of the system
        for i in range(1, n):
            alpha[i] = (3 / h[i] * (y[i + 1] - y[i]) -
                        3 / h[i - 1] * (y[i] - y[i - 1]))

        # Tridiagonal matrix
        l = [1] + [0] * n
        mu = [0] * (n + 1)
        z = [0] * (n + 1)

        for i in range(1, n):
            l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
            mu[i] = h[i] / l[i]
            z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]

        # Step 2: Back substitution to find second derivatives
        l[n] = 1
        z[n] = 0
        c = [0] * (n + 1)
        b = [0] * n
        d = [0] * n

        for j in range(n - 1, -1, -1):
            c[j] = z[j] - mu[j] * c[j + 1]
            b[j] = ((y[j + 1] - y[j]) / h[j] -
                    h[j] * (c[j + 1] + 2 * c[j]) / 3)
            d[j] = (c[j + 1] - c[j]) / (3 * h[j])

        # Step 3: Compute coefficients
        coefficients = []
        for i in range(n):
            a = y[i]
            coefficients.append((a, b[i], c[i], d[i]))

        return coefficients

    def generate_points(self, x, num_points=100):
        """
        Generate evenly spaced points between the minimum and maximum of x.

        Args:
            x (list or array): Input x-coordinates.
            num_points (int): Number of points to generate (default: 100).

        Returns:
            list: A list of evenly spaced points.
        """
        x_min = min(x)
        x_max = max(x)
        return [x_min + i * (x_max - x_min) / (num_points - 1) for i in range(num_points)]

    # Example usage
    x = [0, 1, 2, 3, 4]
    x_new = generate_points(x, num_points=50)  # Generate 50 points dynamically