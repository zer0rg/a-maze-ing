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
        print("\nGenerating...")
        
        # DFS Iterativo: elegir celda inicial aleatoria
        start_x: int = random.randint(1, self.width)
        start_y: int = random.randint(1, self.height)
        start_coord: Coordinate = (start_x, start_y)
        
        # Stack para el DFS iterativo
        stack: list[Coordinate] = [start_coord]
        
        # Marcar la celda inicial como visitada
        self.maze[start_coord].visited = True
        self.visited.add(start_coord)
        
        # Diccionario de direcciones opuestas
        opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        
        step_count = 0
        
        while stack:
            current = stack[-1]
            
            # Obtener vecinos no visitados
            unvisited_neighbors: list[tuple[int, Coordinate]] = []
            
            for direction in [NORTH, SOUTH, EAST, WEST]:
                next_coord = (
                    current[0] + MOVEMENTS[direction][0],
                    current[1] + MOVEMENTS[direction][1]
                )
                nx, ny = next_coord
                
                # Verificar que esté dentro de los límites y no visitada
                if (1 <= nx <= self.width and 1 <= ny <= self.height 
                    and next_coord not in self.visited):
                    unvisited_neighbors.append((direction, next_coord))
            
            if unvisited_neighbors:
                # Elegir un vecino al azar
                direction, next_coord = random.choice(unvisited_neighbors)
                
                # Romper las paredes entre current y next_coord
                self.maze[current].remove_wall(direction)
                self.maze[next_coord].remove_wall(opposites[direction])
                
                # Marcar next_coord como visitada
                self.maze[next_coord].visited = True
                self.visited.add(next_coord)
                
                # Añadir next_coord al stack
                stack.append(next_coord)
                
                step_count += 1
                
                yield {
                    'current': current,
                    'action': 'breaking_wall',
                    'modified_cells': [self.maze[current], self.maze[next_coord]],
                    'message': f'Rompiendo pared {step_count}: {current} -> {next_coord}'
                }
            else:
                # No hay vecinos no visitados, hacer backtrack
                stack.pop()
                if stack:
                    yield {
                        'current': current,
                        'action': 'backtracking',
                        'modified_cells': [self.maze[current]],
                        'message': f'Backtracking desde {current} a {stack[-1]}'
                    }

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
