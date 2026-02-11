from typing import Optional
from self_typing import NORTH, EAST, SOUTH, WEST, MOVEMENTS
from self_typing import MazeWalls, Coordinate, MazeBoard


class Cell:

    def __init__(self, coord: tuple[int, int]):
        self.coord: Coordinate = coord
        self.walls: MazeWalls = NORTH | EAST | SOUTH | WEST
        self.visited: bool = False
        self.is_fixed: bool = False
        self.is_start: bool = False
        self.is_exit: bool = False
        self._neighbors: Optional[dict[int, 'Cell']] = None
        self._maze_ref: Optional['MazeBoard'] = None


    @property
    def neighbors(self) -> dict[int, 'Cell']:
        if self._neighbors is None:
            return {}
        return self._neighbors

    def get_relative_direction(self, other: 'Cell'):
        if self.coord[0] == other.coord[0]:
            if self.coord[1] < other.coord[1]:
                return SOUTH
            else:
                return NORTH
        elif self.coord[1] == other.coord[1]:
            if self.coord[0] < other.coord[0]:
                return EAST
            else:
                return WEST
        else:
            raise ValueError("Cells are not adjacent")


    def set_maze_reference(self, maze: 'MazeBoard') -> None:
        self._maze_ref = maze
        self._calculate_neighbors()

    def add_wall(self, direction: int) -> None:
        """Adds a wall in a direction"""
        self.walls = self.walls | direction

    def has_wall(self, direction: int) -> int:
        """Checks if there is a wall in a direction"""
        return (self.walls & direction)

    def remove_wall(self, direction: int) -> None:
        """Remove a wall in a direction"""
        self.walls = self.walls & ~direction

    def get_accessible_neighbors(self) -> dict[int, 'Cell']:
        """Returns a dict with the accesible neighbors of a Cell"""
        x_1, y_1 = self.coord
        neighbors: dict[int, 'Cell'] = {}
        for direction, move in MOVEMENTS.items():
            if not self.has_wall(direction) and self._maze_ref:
                x_2, y_2 = move
                neighbors[direction] = self._maze_ref[(x_1 + x_2, y_2 + y_1)]

        return neighbors

    def _calculate_neighbors(self) -> None:
        if self._maze_ref is None:
            return

        self._neighbors = {}
        for direction in [NORTH, EAST, SOUTH, WEST]:
            neighbor_coord = (
                self.coord[0] + MOVEMENTS[direction][0],
                self.coord[1] + MOVEMENTS[direction][1]
            )
            if neighbor_coord in self._maze_ref:
                self._neighbors[direction] = self._maze_ref[neighbor_coord]


    def __eq__(self, value):
        if not isinstance(value, Cell):
            return False
        return self.coord == value.coord

    def __hash__(self):
        return hash(self.coord)

    def __str__(self):
        return f"Cell({self.coord}, walls={self.walls}, visited={self.visited})"
