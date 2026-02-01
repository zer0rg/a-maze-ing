from typing import Dict, Tuple, TypeAlias


# Constantes para las direcciones bit a bit
NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

# Tipos de dato para el laberinto
MazeCell: TypeAlias = int
Coordinate: TypeAlias = Tuple[int, int]
MazeBoard: TypeAlias = Dict[Coordinate, MazeCell]


__all__ = ['MazeCell', 'MazeBoard', 'Coordinate', 'NORTH', 'EAST', 'SOUTH',
           'WEST']
