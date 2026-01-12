from abc import ABC, abstractmethod
from typing import List

from maze_types.maze import Coordinate, MazeBoard, movements

class MazeSolver(ABC):

    def __init__(self, board: MazeBoard, entry: Coordinate, exit: Coordinate):
        self.board: MazeBoard = board
        self.entry: Coordinate = entry
        self.exit: Coordinate = exit

    @abstractmethod
    def solve(self):
        pass

    def get_rows(self):
        try:
            return max(x for x, y in self.board.keys())
        except ValueError:
            return -1

    def get_cols(self):
        try:
            return max(y for x, y in self.board.keys())
        except ValueError:
            return -1