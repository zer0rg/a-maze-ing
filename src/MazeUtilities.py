from abc import ABC, abstractmethod
from typing import List

from maze_types import Coordinate, movements, MazeBoard
from maze_types.maze import NORTH


class MazeUtilities(ABC):
    @staticmethod
    def get_neighbors(coord: Coordinate, maze_board: MazeBoard) -> list[tuple[int, int]] | None:
        neighbors: List[Coordinate] = []
        x_1, y_1 = coord
        cell_info = maze_board[(x_1, y_1)]
        for direction, move in movements.items():
            if not MazeUtilities.has_wall(cell_info, direction):
                x_2, y_2 = move
                neighbors.append((x_1 + x_2, y_2 + y_1))
        return neighbors

    @staticmethod
    def has_wall(cell: int, direction: int) -> bool:
        return bool(cell & direction)
