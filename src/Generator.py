from collections import deque
import time
from custom_typing.maze import MOVEMENTS, MazeBoard, Coordinate, NORTH, EAST, SOUTH, WEST
from src.Config import Config
from src.Cell import Cell
import random


class Generator:

    def __init__(self, config: Config):
        self.width: int = config.width
        self.height: int = config.height
        self.perfect: bool = config.perfect
        self.entry: Coordinate = config.entry
        self.exit: Coordinate = config.exit
        self.output_file: str = config.output_file
        self.maze: MazeBoard = {}
        self.initialize_board()

    def generate(self) -> None:
        """
        Genera el laberinto completo usando algoritmo DFS iterativo.
        Modifica directamente self.maze sin emitir eventos.
        """
        print("\nGenerating...")
        # DFS Iterativo: elegir celda inicial aleatoria
        start_x: int = random.randint(1, self.width)
        start_y: int = random.randint(1, self.height)
        start_coord: Coordinate = (start_x, start_y)

        # Stack para el DFS iterativo usando Cell directamente
        start_cell: Cell = self.maze[start_coord]
        stack: list[Cell] = [start_cell]

        # Marcar la celda inicial como visitada
        start_cell.visited = True

        # Diccionario de direcciones opuestas
        opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

        while stack:
            current_cell = stack[-1]

            # Obtener vecinos no visitados directamente desde la celda
            unvisited_neighbors: list[tuple[int, Cell]] = []
            for direction, neighbor in current_cell.neighbors.items():
                if not neighbor.visited and not neighbor.is_fixed:
                    unvisited_neighbors.append((direction, neighbor))

            if unvisited_neighbors:
                direction, next_cell = random.choice(unvisited_neighbors)

                # Romper las paredes entre current_cell y next_cell
                current_cell.remove_wall(direction)
                next_cell.remove_wall(opposites[direction])

                # Marcar next_cell como visitada
                next_cell.visited = True

                # Añadir next_cell al stack
                stack.append(next_cell)
            else:
                # No hay vecinos no visitados, hacer backtrack
                stack.pop()


    def generate_step_by_step(self):
        """
        Genera el laberinto usando algoritmo DFS
        Devuelve un stream en cada pared que el algoritmo rompe
        con las celdas modificadas
        """
        print("\nGenerating...")
        print("Press Q in the maze window to abort generation")
        # DFS Iterativo: elegir celda inicial aleatoria
        start_x: int = random.randint(1, self.width)
        start_y: int = random.randint(1, self.height)
        start_coord: Coordinate = (start_x, start_y)

        # Stack para el DFS iterativo usando Cell directamente
        start_cell: Cell = self.maze[start_coord]
        stack: list[Cell] = [start_cell]

        # Marcar la celda inicial como visitada
        start_cell.visited = True

        # Diccionario de direcciones opuestas
        opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

        while stack:
            current_cell = stack[-1]

            # Obtener vecinos no visitados directamente desde la celda
            unvisited_neighbors: list[tuple[int, Cell]] = []
            for direction, neighbor in current_cell.neighbors.items():
                if not neighbor.visited and not neighbor.is_fixed:
                    unvisited_neighbors.append((direction, neighbor))

            if unvisited_neighbors:
                direction, next_cell = random.choice(unvisited_neighbors)


                # Romper las paredes entre current_cell y next_cell
                current_cell.remove_wall(direction)
                next_cell.remove_wall(opposites[direction])

                # Marcar next_cell como visitada
                next_cell.visited = True

                # Añadir next_cell al stack
                stack.append(next_cell)

                yield {
                    'current': current_cell.coord,
                    'action': 'breaking_wall',
                    'modified_cells': [current_cell, next_cell],
                }
            else:
                # No hay vecinos no visitados, hacer backtrack
                stack.pop()
                if stack:

                    yield {
                        'current': current_cell.coord,
                        'action': 'backtracking',
                        'modified_cells': [current_cell],
                    }
        if not self.perfect:
            print("\nAdding extra paths...")
            extra_path = self._add_extra_paths()
            for cell in extra_path:
                yield {
                    'current': cell.coord,
                    'action': 'adding_extra_path',
                    'modified_cells': [cell],
                }
        print(f"[OK] Maze generated successfully")

    def bfs_distance(self, start: Cell, end: Cell, max_dist: int = 10) -> int:
        """Distancia BFS entre start y end respetando paredes"""
        queue = deque([(start, 0)])
        visited = set()
        while queue:
            current, dist = queue.popleft()
            if current.coord == end.coord:
                return dist
            if current.coord in visited or dist > max_dist:
                continue
            visited.add(current.coord)
            for direction, neighbor in current.neighbors.items():
                if not current.has_wall(direction):
                    queue.append((neighbor, dist + 1))
        return float('inf')  # No hay camino

    def _add_extra_paths(self, min_dist: int = 6, max_paths: int = 10) -> list[Cell]:
        """Agrega caminos extra evitando ciclos triviales"""
        candidates = []

        # Paso 1: recolectar todas las paredes candidatas
        for cell in self.maze.values():
            for direction, neighbor in cell.neighbors.items():
                if not cell.is_fixed and not neighbor.is_fixed and cell.has_wall(direction):
                    candidates.append((cell, neighbor, direction))

        random.shuffle(candidates)

        extra_path_cells = []
        added = 0

        # Paso 2: romper paredes si distancia es suficientemente larga
        for cell, neighbor, direction in candidates:
            if added >= max_paths:
                break
            dist = self.bfs_distance(cell, neighbor, max_dist=5)
            if dist >= min_dist:
                cell.remove_wall(direction)
                OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
                neighbor.remove_wall(OPPOSITE[direction])
                extra_path_cells.extend([cell, neighbor])
                added += 1

        return extra_path_cells

    def initialize_board(self) -> None:
        """Inicializa el laberinto con todas las paredes cerradas"""
        center_x: int = (self.width + 1) // 2
        center_y: int = (self.height + 1) // 2
        center_coord: Coordinate = (center_x, center_y)

        logo_pattern: list[Coordinate] = [
            # Número "4"
            (-3, -2), (-3, -1), (-3, 0),  # Línea vertical izquierda
            (-2, 0),  # Línea horizontal media
            (-1, 0), (-1, 1), (-1, 2),  # Línea vertical derecha

            # Separación

            # Número "2"
            (1, -2), (2, -2), (3, -2),  # Línea superior
            (3, -1),  # Bajada derecha
            (1, 0), (2, 0), (3, 0),  # Línea media
            (1, 1),  # Bajada izquierda
            (1, 2), (2, 2), (3, 2),  # Línea inferior
        ]
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                self.maze[(x, y)] = Cell((x, y))
                if (x, y) == self.entry:
                    self.maze[(x, y)].is_start = True
                if (x, y) == self.exit:
                    self.maze[(x, y)].is_exit = True

        for coord in logo_pattern:
            fixed_coord: Coordinate = (center_coord[0] + coord[0],
                                       center_coord[1] + coord[1])
            self.maze[fixed_coord].is_fixed = True

        for cell in self.maze.values():
            cell.set_maze_reference(self.maze)
