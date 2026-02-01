from abc import ABC, abstractmethod

from self_typing import Coordinate, MazeBoard


class MazeSolver(ABC):

    def __init__(self, board: MazeBoard, entry: Coordinate, exit: Coordinate):
        self.board: MazeBoard = board
        self.entry: Coordinate = entry
        self.exit: Coordinate = exit
        self.path = None

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def reconstruct_path(self, *args, **kwargs): pass

    def get_path_moves(self):
        moves = []
        i = 0
        while self.path[i] != self.exit:
            actual = self.path[i]
            next = self.path[i + 1]
            if actual + (0, -1) == next:
                moves.append(1)  # NORTH
            elif actual + (1, 0) == next:
                moves.append(2)  # EAST
            elif actual + (0, 1) == next:
                moves.append(4)  # SOUTH
            elif actual + (-1, 0) == next:
                moves.append(8)  # WEST
            i += 1
        return moves
