from abc import ABC
from typing import List

from maze_types import Coordinate, MOVEMENTS, MazeBoard


class MazeUtilities(ABC):

    @staticmethod
#   Devuelve una lista con las celdas vecinas que no tienen pared entre sí
    def get_neighbors(
            coord: Coordinate,
            maze_board: MazeBoard
    ) -> list[tuple[int, int]]:
        neighbors: List[Coordinate] = []
        x_1, y_1 = coord
        cell = maze_board[(x_1, y_1)]
        for direction, move in MOVEMENTS.items():
            if not MazeUtilities.has_wall(cell, direction):
                x_2, y_2 = move
                neighbors.append((x_1 + x_2, y_2 + y_1))
        return neighbors

    @staticmethod
#   Verfica si la celda tiene pared en esa direccion
    def has_wall(cell: int, direction: int) -> bool:
        return bool(cell & direction)

    @staticmethod
#   Elimina una pared de una celda en una direccion
    def remove_wall(cell: int, direction: int) -> int:
        return cell & ~direction

    @staticmethod
#   Añade una pared a una celda
    def add_wall(cell: int, direction: int) -> int:
        """Añade una pared a una celda"""
        return cell | direction

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
