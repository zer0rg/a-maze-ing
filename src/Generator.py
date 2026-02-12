"""Maze generator module using DFS algorithm."""

from collections import deque
from typing import TypeAlias, Generator as GenType, Any
from custom_typing.maze import MazeBoard, Coordinate, NORTH, EAST, SOUTH, WEST
from src.Config import Config
from src.Cell import Cell
import random

# TypeAlias for unvisited neighbors and wall candidates
UnvisitedNeighbors: TypeAlias = list[tuple[int, Cell]]
WallCandidate: TypeAlias = tuple[Cell, Cell, int]
GeneratorStep: TypeAlias = dict[str, Any]


class Generator:
    """Maze generator using iterative DFS algorithm."""

    def __init__(self, config: Config):
        """Initialize the generator with configuration settings."""
        self.width: int = config.width
        self.height: int = config.height
        self.perfect: bool = config.perfect
        self.entry: Coordinate = config.entry
        self.exit: Coordinate = config.exit
        self.output_file: str = config.output_file
        self.seed: int | None = config.seed
        self.maze: MazeBoard = {}
        self.initialize_board()

    def _init_random(self) -> None:
        """Initialize random generator with seed if provided."""
        if self.seed is not None:
            random.seed(self.seed)

    def generate(self) -> None:
        """Generate the complete maze using iterative DFS algorithm."""
        print("\nGenerating...")
        self._init_random()
        # Iterative DFS: choose random initial cell
        start_x: int = random.randint(1, self.width)
        start_y: int = random.randint(1, self.height)
        start_coord: Coordinate = (start_x, start_y)

        # Stack for iterative DFS using Cell directly
        start_cell: Cell = self.maze[start_coord]
        stack: list[Cell] = [start_cell]

        # Mark initial cell as visited
        start_cell.visited = True

        # Dictionary of opposite directions
        opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

        while stack:
            current_cell = stack[-1]

            # Get unvisited neighbors directly from cell
            unvisited_neighbors: UnvisitedNeighbors = []
            for direction, neighbor in current_cell.neighbors.items():
                if not neighbor.visited and not neighbor.is_fixed:
                    unvisited_neighbors.append((direction, neighbor))

            if unvisited_neighbors:
                direction, next_cell = random.choice(unvisited_neighbors)

                # Break walls between current_cell and next_cell
                current_cell.remove_wall(direction)
                next_cell.remove_wall(opposites[direction])

                # Mark next_cell as visited
                next_cell.visited = True

                # Add next_cell to stack
                stack.append(next_cell)
            else:
                # No unvisited neighbors, backtrack
                stack.pop()
        if not self.perfect:
            print("\nAdding extra paths...")
            self._add_extra_paths()

    def generate_step_by_step(self) -> GenType[GeneratorStep, None, None]:
        """Generate the maze using DFS yielding each step for animation."""
        print("\nGenerating...")
        print("Press Q in the maze window to abort generation")
        self._init_random()
        # Iterative DFS: choose random initial cell
        start_x: int = random.randint(1, self.width)
        start_y: int = random.randint(1, self.height)
        start_coord: Coordinate = (start_x, start_y)

        # Stack for iterative DFS using Cell directly
        start_cell: Cell = self.maze[start_coord]
        stack: list[Cell] = [start_cell]

        # Mark initial cell as visited
        start_cell.visited = True

        # Dictionary of opposite directions
        opposites = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

        while stack:
            current_cell = stack[-1]

            # Get unvisited neighbors directly from cell
            unvisited_neighbors: UnvisitedNeighbors = []
            for direction, neighbor in current_cell.neighbors.items():
                if not neighbor.visited and not neighbor.is_fixed:
                    unvisited_neighbors.append((direction, neighbor))

            if unvisited_neighbors:
                direction, next_cell = random.choice(unvisited_neighbors)

                # Break walls between current_cell and next_cell
                current_cell.remove_wall(direction)
                next_cell.remove_wall(opposites[direction])

                # Mark next_cell as visited
                next_cell.visited = True

                # Add next_cell to stack
                stack.append(next_cell)

                yield {
                    'current': current_cell.coord,
                    'action': 'breaking_wall',
                    'modified_cells': [current_cell, next_cell],
                }
            else:
                # No unvisited neighbors, backtrack
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

    def bfs_distance(self, start: Cell, end: Cell, max_dist: int = 10) -> int:
        """Calculate BFS distance between two cells respecting walls."""
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
        return 999999  # No path found

    def _add_extra_paths(self, min_dist: int = 6,
                         max_paths: int = 10) -> list[Cell]:
        """Add extra paths avoiding trivial cycles."""
        candidates = []

        # Step 1: collect all candidate walls
        for cell in self.maze.values():
            for direction, neighbor in cell.neighbors.items():
                if not cell.is_fixed and not neighbor.is_fixed and (
                        cell.has_wall(direction)):
                    candidates.append((cell, neighbor, direction))

        random.shuffle(candidates)

        extra_path_cells = []
        added = 0

        # Step 2: break walls if distance is long enough
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
        """Initialize the maze with all walls closed."""
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
