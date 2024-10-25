
class UniversalParent:

    def __init__(self):
        #TBH. Still Zero clue what EXACTLY these do. They seem arbitrary at a glance..
        # Will be handled once everything is working. May go to config if it matters. If else they will be removed.
        self.file_name = "UNIVERSAL PARENT"
        self.extension = 'UNKNOWN'
        # TILL FIGURED OUT HOW THIS CHANGES IT LIVES HERE
        self.SIZE = 1  # WAS SIZE
        self.WIDTH = 1  # WAS WIDTH
        self.HEIGHT = 2  # WAS HEIGHT
        self.NVERTS = 10  # NVERTS

        # numerical roundoff tolerance for testing intersections
        self.EPS = 1e-20

        # No clue what this does...
        self.X = 0
        # No clue what this does...
        self.Y = 1

        # GOTTEN FROM THE PARSED INFILE....
        # USED to determine the type of Aperture Hole
        # 'C': Circle
        # 'R': Rectangle
        # 'O': Obround
        self.TYPE = 0

        # UNIT: METRIC OR IMPERIAL
        # 0 (METRIC) is default
        # 1 (IMPERIAL) is an option. :(
        self._unit = 0

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, new_value):
        if new_value == 0 or new_value == 1:
            self._unit = new_value
        else:
            raise ValueError(f"{self.file_name}: \"unit\" must be equal to 0/1.")
