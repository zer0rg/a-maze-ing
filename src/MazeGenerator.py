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
        
        # Diccionario de direcciones opuestas
        opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        
        step_count = 0
        
        while stack:
            current = stack[-1]
            current_cell = self.maze[current]
            
            # Obtener vecinos no visitados directamente desde la celda
            unvisited_neighbors: list[tuple[int, Cell]] = [
                (direction, neighbor)
                for direction, neighbor in current_cell.neighbors.items()
                if not neighbor.visited
            ]
            
            if unvisited_neighbors:
                direction, next_cell = random.choice(unvisited_neighbors)
                
                # Romper las paredes entre current y next_cell
                current_cell.remove_wall(direction)
                next_cell.remove_wall(opposites[direction])
                
                # Marcar next_cell como visitada
                next_cell.visited = True
                
                # Añadir next_cell al stack
                stack.append(next_cell.coord)
                
                step_count += 1
                
                yield {
                    'current': current,
                    'action': 'breaking_wall',
                    'modified_cells': [current_cell, next_cell],
                    'message': f'Rompiendo pared {step_count}: {current} -> {next_cell.coord}'
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
                if (x, y) == self.entry:
                    maze[(x, y)].isStart = True
                if (x, y) == self.exit:
                    maze[(x, y)].isExit = True

        for cell in maze.values():
            cell.set_maze_reference(maze)

        return maze
