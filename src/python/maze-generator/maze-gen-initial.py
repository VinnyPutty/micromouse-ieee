# 3.1 Maze Dimensions
# The maze is composed of 18cm x 18cm unit squares
# arranged as 16 x 16 units. The walls of the units of the
# maze are 5 cm high and 1.2 cm thick (assume 5%
# tolerance for mazes). The outside wall encloses the
# entire maze.


class Tile:
    def __init__(self, side_length=18, wall_height=5, wall_thickness=1.2):
        self.left_wall: bool = False
        self.top_wall: bool = False
        self.right_wall: bool = False
        self.bottom_wall: bool = False


class Maze:
    def __init__(self, size=16, perimeter_overlap=False):
        self.maze = None

