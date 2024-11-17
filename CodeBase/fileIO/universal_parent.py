
class UniversalParent:

    def __init__(self):
        ## IS THIS STUFF INPORTANT?? REVIEW*************
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
