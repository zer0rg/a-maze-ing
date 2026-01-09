from typing import Dict, Tuple, TypeAlias

MazeCell: TypeAlias = Dict[str, bool]
Coordinate: TypeAlias = Tuple[int, int]
#  {(x, y) : {'N': True, 'E': True, 'S': True, 'W': True}}
#  No se que tal te parece esta forma de representar cada celda,
#  ami me mola :)
MazeBoard: TypeAlias = Dict[Coordinate, MazeCell]
