from self_typing.maze import MazeBoard, Coordinate, NORTH, EAST, SOUTH, WEST
from self_typing.maze import MOVEMENTS
from src.MazeConfig import MazeConfig
from src.Cell import Cell
import random


class MazeGenerator:

    def __init__(self, config: MazeConfig):
        self.width: int = config.width
        self.height: int = config.height
        self.perfect: bool = config.perfect
        self.entry: Coordinate = config.entry
        self.exit: Coordinate = config.exit
        self.output_file: str = config.output_file
        print(f"[...] Creating {self.width}x{self.height} maze...")
        self.maze: MazeBoard = self._initialize_board()
        print(f"[OK] Board initialized with {len(self.maze)} cells")
        self.visited: set = set()

    def generate_step_by_step(self):
        # Simula 50 roturas aleatorias para probar el stream con yield
        # (ALGORITMO FINAL TODO)
        for i in range(50):
            # Elegir una celda aleatoria
            x = random.randint(1, self.width)
            y = random.randint(1, self.height)
            current = (x, y)

            if current not in self.maze:
                continue

            # Marcar como visitada
            self.maze[current].visited = True

            # Elegir una dirección aleatoria
            directions = [NORTH, SOUTH, EAST, WEST]
            random.shuffle(directions)
            opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

            for direction in directions:
                next_coord = (current[0] + MOVEMENTS[direction][0],
                              current[1] + MOVEMENTS[direction][1])

                nx, ny = next_coord
                if 1 <= nx <= self.width and 1 <= ny <= self.height:
                    # Romper la pared
                    self.maze[current].remove_wall(direction)
                    self.maze[next_coord].remove_wall(opposites[direction])
                    self.maze[next_coord].visited = True

                    yield {
                        'current': current,
                        'action': 'breaking_wall',
                        'modified_cells': self.maze,
                        'message': f'Rompiendo pared {i+1}/50: {current} -> \
{next_coord}'
                    }
                    break

    def _add_extra_paths(self):
        # TODO
        pass

    def _initialize_board(self) -> MazeBoard:
        maze: MazeBoard = {}

        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                maze[(x, y)] = Cell((x, y))

        for cell in maze.values():
            cell.set_maze_reference(maze)

        return maze
