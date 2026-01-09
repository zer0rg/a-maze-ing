from types.maze import MazeBoard, Coordinate, NORTH, EAST, SOUTH, WEST
from src.MazeConfig import MazeConfig
from src.OutputFileHandler import OutputFileHandler


class MazeGenerator:

    def __init__(self, config: MazeConfig):
        self.width: int = config.width
        self.height: int = config.height
        self.perfect: bool = config.perfect
        self.entry: Coordinate = config.entry
        self.exit: Coordinate = config.exit
        self.output_file: str = config.output_file
        self.maze: MazeBoard = self._initialize_board()

    def generate(self) -> MazeBoard:
        pass
#       Podemos generar un laberinto perfecto con backtracking recursivo,
#       y si PERFECT=FALSE añadimos caminos extra de alguna manera???
        return self.maze

    def save_to_file(self):
        with open(self.output_file, "w") as output_file:
            OutputFileHandler().save_file(output_file)

    def _initialize_board(self) -> MazeBoard:
        maze: MazeBoard = {}
        for y in range(self.height):
            for x in range(self.width):
                maze[(x, y)] = NORTH | EAST | SOUTH | WEST
        return maze

#   Verfica si la celda tiene pared en esa direccion
    @staticmethod
    def has_wall(cell: int, direction: int) -> bool:
        return bool(cell & direction)

#   Elimina una pared de una celda en una direccion
    @staticmethod
    def remove_wall(cell: int, direction: int) -> int:
        return cell & ~direction

#   Añade una pared a una celda
    @staticmethod
    def add_wall(cell: int, direction: int) -> int:
        """Añade una pared a una celda"""
        return cell | direction
