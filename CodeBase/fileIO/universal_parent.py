class UniversalParent:

    def __init__(self):
        #TBH. Still Zero clue what EXACTLY these do. They seem arbitrary at a glance..
        # Will be handled once everything is working. May go to config if it matters. If else they will be removed.

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