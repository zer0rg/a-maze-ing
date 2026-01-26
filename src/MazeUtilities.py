from abc import ABC
from typing import List

from self_typing.maze import Coordinate, MOVEMENTS, MazeBoard


class MazeUtilities(ABC):

    @staticmethod
#   Devuelve las filas de un laberinto
    def get_rows(maze_board: MazeBoard):
        try:
            return max(x for x, y in maze_board.keys())
        except ValueError:
            return -1

#   Devuelve las columnas de un laberinto
    @staticmethod
    def get_cols(self):
        try:
            return max(y for x, y in self.board.keys())
        except ValueError:
            return -1
