class ApertureParent:
    def __init__(self):
        self.aperture_type = None
        self.aperture_number = None
        self.inner_hole_diameter = None
        pass

    # Comparison function to make objects comparable based on aperture_number
    def __lt__(self, other):
        return self.aperture_number < other.aperture_number
