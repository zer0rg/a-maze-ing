from maze_types.maze import MazeBoard, Coordinate, NORTH, EAST, SOUTH, WEST
from maze_types.maze import MOVEMENTS
from src.MazeConfig import MazeConfig
from src.OutputFileHandler import OutputFileHandler
from src.MazeUtilities import MazeUtilities
import random


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
        x, y = coord

        if x < 1 or y < 1 or x > self.width or y > self.height:
            return

        if coord in self.visited:
            return
        # Marcar la celda actual como visitada
        self.visited.add(coord)
        # Crear lista de direcciones y aleatorizarla
        directions = [NORTH, SOUTH, EAST, WEST]
        random.shuffle(directions)
        # Diccionario de direcciones opuestas
        opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        # Iterar sobre las direcciones en orden aleatorio
        for direction in directions:
            next_coord = (coord[0] + MOVEMENTS[direction][0],
                          coord[1] + MOVEMENTS[direction][1])

            nx, ny = next_coord
        # Verificar si la siguiente celda está dentro de limites y no visitada
            if (1 <= nx <= self.width and 1 <= ny <= self.height
                    and next_coord not in self.visited):
                # Romper la pared de la celda actual hacia la dirección
                self.maze[coord] = MazeUtilities.remove_wall(
                    self.maze[coord], direction)
                # Romper la pared opuesta de la celda destino
                self.maze[next_coord] = MazeUtilities.remove_wall(
                    self.maze[next_coord], opposites[direction])
                self._init_backtracking(next_coord)

    def save_to_file(self):
        with open(self.output_file, "w") as output_file:
            OutputFileHandler().save_file(output_file)

    def _initialize_board(self) -> MazeBoard:
        maze: MazeBoard = {}
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                maze[(x, y)] = NORTH | EAST | SOUTH | WEST
        return maze
