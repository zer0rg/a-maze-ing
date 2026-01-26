from self_typing.maze import MazeBoard, Coordinate, NORTH, EAST, SOUTH, WEST
from self_typing.maze import MOVEMENTS
from src.MazeConfig import MazeConfig
from src.MazeUtilities import MazeUtilities
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
        self.maze: MazeBoard = self._initialize_board()
        self.visited: set = set()

    def generate(self):
        self._init_backtracking(self.entry)
        # Si el laberinto no tiene que ser perfecto deberemos añadir
        # nuevas rutas TODO
        if not self.perfect:
            self._add_extra_paths()
        
        return self.maze

    def generate_step_by_step(self):
        """
        Generador que yield el estado del maze en cada paso.
        Por ahora solo muestra el maze inicializado (todas las paredes cerradas).
        """
        # Yield el estado inicial con todas las celdas cerradas
        yield {
            'current': (1, 1),
            'action': 'initialized',
            'message': 'Laberinto inicializado con todas las paredes'
        }

    def _add_extra_paths(self):
        # TODO
        pass

    def _init_backtracking(self, coord: Coordinate):
            stack = [coord]
            
            while stack:  # Mientras la pila no esté vacía
                current = stack[-1]  # Ver el último elemento sin sacarlo
                x, y = current

                if x < 1 or y < 1 or x > self.width or y > self.height:
                    stack.pop()
                    continue

                if self.maze[current].visited:
                    stack.pop()
                    continue
                    
                self.maze[current].visited = True
                
                directions = [NORTH, SOUTH, EAST, WEST]
                random.shuffle(directions)
                opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
                
                found_unvisited: bool = False
                # Iterar sobre las direcciones en orden aleatorio
                for direction in directions:
                    next_coord = (current[0] + MOVEMENTS[direction][0],
                                current[1] + MOVEMENTS[direction][1])

                    nx, ny = next_coord
                    # Verificar si la siguiente celda esta dentro de limites y no visitada
                    if (1 <= nx <= self.width and 1 <= ny <= self.height
                            and next_coord not in self.visited):
                        # Romper la pared de la celda actual hacia la dirección
                        self.maze[current].remove_wall(direction)
                        # Romper la pared opuesta de la celda destino
                        self.maze[next_coord].remove_wall(opposites[direction])
                        
                        stack.append(next_coord)  # Añadir a la pila
                        found_unvisited = True
                        break 
                
                if not found_unvisited:
                    stack.pop()

    def _initialize_board(self) -> MazeBoard:
        maze: MazeBoard = {}

        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                maze[(x, y)] = Cell((x, y))
    
        for cell in maze.values():
            cell.set_maze_reference(maze)

        return maze
