from typing.maze import MazeBoard, Coordinate, NORTH, EAST, SOUTH, WEST
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
        # Set de datos para marcar las casillas ya visitadas
        self.visited: set = set()

    def generate(self) -> MazeBoard:
        self._init_backtracking(self.entry)
        return self.maze

    def _init_backtracking(self, coord: Coordinate):
        # La idea es desde un punto inicial buscar si uno de su adyacentes
        # se ha visitado y si no ha visitado romper la pared que les separa
        # y seguir para adelante asi hasta pasar por todas las casillas
        x, y = coord

        if x < 1 or y < 1 or x > self.width or y > self.height:
            return

        if coord in self.visited:
            return

        self.visited.add(coord)

    def save_to_file(self):
        with open(self.output_file, "w") as output_file:
            OutputFileHandler().save_file(output_file)

    def _initialize_board(self) -> MazeBoard:
        maze: MazeBoard = {}
        for y in range(self.height):
            for x in range(self.width):
                maze[(x, y)] = NORTH | EAST | SOUTH | WEST
        return maze
