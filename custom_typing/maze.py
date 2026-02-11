from typing import Dict, Tuple, TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from src.Cell import Cell


# Constantes para las direcciones bit a bit
NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

MOVEMENTS = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0),
}

# Tipos de dato para el laberinto
MazeWalls: TypeAlias = int
Coordinate: TypeAlias = Tuple[int, int]
MazeBoard: TypeAlias = Dict[Coordinate, 'Cell']


__all__ = ['MazeWalls', 'MazeBoard', 'Coordinate', 'NORTH', 'EAST', 'SOUTH',
           'WEST']
