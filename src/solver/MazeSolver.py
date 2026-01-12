from abc import ABC, abstractmethod

from typing.maze import Coordinate, MazeBoard


class MazeSolver(ABC):

    def __init__(self, board: MazeBoard, entry: Coordinate, exit: Coordinate):
        self.board: MazeBoard = board
        self.entry: Coordinate = entry
        self.exit: Coordinate = exit

    @abstractmethod
    def solve(self):
        pass
