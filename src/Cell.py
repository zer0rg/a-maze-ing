"""Cell module for maze representation."""

from typing import Optional, TypeAlias
from custom_typing import NORTH, EAST, SOUTH, WEST, MOVEMENTS
from custom_typing import MazeWalls, Coordinate, MazeBoard

# TypeAlias for neighbor mapping
NeighborMap: TypeAlias = dict[int, 'Cell']


class Cell:
    """Represents a single cell in the maze."""

    def __init__(self, coord: tuple[int, int]) -> None:
        """Initialize a cell with coordinates and default walls."""
        self.coord: Coordinate = coord
        self.walls: MazeWalls = NORTH | EAST | SOUTH | WEST
        self.visited: bool = False
        self.is_fixed: bool = False
        self.is_start: bool = False
        self.is_exit: bool = False
        self._neighbors: Optional[NeighborMap] = None
        self._maze_ref: Optional['MazeBoard'] = None

    @property
    def neighbors(self) -> NeighborMap:
        """Return the neighbors of this cell."""
        if self._neighbors is None:
            return {}
        return self._neighbors

    def get_relative_direction(self, other: 'Cell') -> int:
        """Return the direction from this cell to another adjacent cell."""
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
        """Set the maze reference and calculate neighbors."""
        self._maze_ref = maze
        self._calculate_neighbors()

    def add_wall(self, direction: int) -> None:
        """Add a wall in the specified direction."""
        self.walls = self.walls | direction

    def has_wall(self, direction: int) -> int:
        """Check if there is a wall in the specified direction."""
        return (self.walls & direction)

    def remove_wall(self, direction: int) -> None:
        """Remove a wall in the specified direction."""
        self.walls = self.walls & ~direction

    def get_accessible_neighbors(self) -> NeighborMap:
        """Return a dict with the accessible neighbors of this cell."""
        x_1, y_1 = self.coord
        neighbors: NeighborMap = {}
        for direction, move in MOVEMENTS.items():
            if not self.has_wall(direction) and self._maze_ref:
                x_2, y_2 = move
                neighbors[direction] = self._maze_ref[(x_1 + x_2, y_2 + y_1)]

        return neighbors

    def _calculate_neighbors(self) -> None:
        """Calculate and cache all neighbor cells."""
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

    def __eq__(self, value: object) -> bool:
        """Check equality based on coordinates."""
        if not isinstance(value, Cell):
            return False
        return self.coord == value.coord

    def __hash__(self) -> int:
        """Return hash based on coordinates."""
        return hash(self.coord)

    def __str__(self) -> str:
        """Return string representation of the cell."""
        return f"Cell({self.coord}, walls={self.walls}, \
visited={self.visited})"
