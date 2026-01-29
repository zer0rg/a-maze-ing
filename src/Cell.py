from typing import Optional
from self_typing import NORTH, EAST, SOUTH, WEST, MOVEMENTS
from self_typing import MazeWalls, Coordinate, MazeBoard


class Cell:

    def __init__(self, coord: tuple[int, int]):
        self.coord: Coordinate = coord
        self.walls: MazeWalls = NORTH | EAST | SOUTH | WEST
        self.visited: bool = False
        self.isFixed: bool = False
        self._neighbors: Optional[dict[int, 'Cell']] = None
        self._maze_ref: Optional['MazeBoard'] = None

    @property
    def neighbors(self) -> dict[int, 'Cell']:
        if self._neighbors is None:
            return {}
        return self._neighbors

    def set_maze_reference(self, maze: 'MazeBoard') -> None:
        self._maze_ref = maze
        self._calculate_neighbors()

    def add_wall(self, direction: int) -> None:
        self.walls = self.walls | direction

    def has_wall(self, direction: int) -> int:
        return (self.walls & direction)

    def remove_wall(self, direction: int) -> None:
        self.walls = self.walls & ~direction

    def get_accessible_neighbors(self) -> dict[int, 'Cell']:
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
