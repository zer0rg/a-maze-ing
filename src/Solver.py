from collections import deque
from typing import Dict, Generator, List, Optional, Set, TypeAlias, Any
from custom_typing.maze import Coordinate, MazeBoard
from src.Cell import Cell

# TypeAlias para clarificar el propósito de las estructuras de datos
ParentMap: TypeAlias = Dict[Cell, Optional[Cell]]
VisitedSet: TypeAlias = Set[Cell]
SolveStep: TypeAlias = Dict[str, Any]


class Solver:

    def __init__(self, board: MazeBoard, entry: Coordinate, exit: Coordinate):
        self.board = board
        self.entry = entry
        self.exit = exit
        self.reconstructed_path: Optional[list[Cell]] = None

    def solve(self) -> Optional[List[Cell]]:
        """
        Resuelve el laberinto usando BFS bidireccional de forma completa.
        Retorna el camino de solución o None si no existe.
        """
        print("\nSolving maze...")
        start = self.board.get(self.entry)
        goal = self.board.get(self.exit)

        if start is None or goal is None:
            print("[ERROR] Invalid entry or exit coordinates")
            return None

        queue_start = deque([start])
        queue_goal = deque([goal])
        parent_start: ParentMap = dict()
        parent_start[start] = None
        parent_goal: ParentMap = dict()
        parent_goal[goal] = None
        visited_start: VisitedSet = {start}
        visited_goal: VisitedSet = {goal}

        while queue_start and queue_goal:
            # Verificar si se encontró el punto de encuentro
            for visited in visited_start:
                if visited in visited_goal:
                    path = self.reconstruct_path(
                        parent_start, parent_goal, visited
                    )
                    self.reconstructed_path = path
                    print(f"[OK] Solution found! Path length: {len(path)}")
                    return path

            # Expandir desde el inicio
            node_start = queue_start.popleft()
            for neighbor in node_start.get_accessible_neighbors().values():
                if neighbor not in visited_start:
                    queue_start.append(neighbor)
                    visited_start.add(neighbor)
                    parent_start[neighbor] = node_start

            # Expandir desde el objetivo
            node_goal = queue_goal.popleft()
            for neighbor in node_goal.get_accessible_neighbors().values():
                if neighbor not in visited_goal:
                    queue_goal.append(neighbor)
                    visited_goal.add(neighbor)
                    parent_goal[neighbor] = node_goal

        print("[ERROR] No solution found")
        return None

    def solve_step_by_step(self) -> Generator[SolveStep, None, None]:
        """Generate the solution step by step using bidirectional BFS."""
        print("\nSolving...")
        print("Press Q in the maze window to abort solving")

        start = self.board.get(self.entry)
        goal = self.board.get(self.exit)

        if start is None or goal is None:
            print("[ERROR] Invalid entry or exit coordinates")
            yield {
                'current': None,
                'action': 'no_solution',
                'modified_cells': [],
            }
            return

        queue_start = deque([start])
        queue_goal = deque([goal])
        parent_start: ParentMap = dict()
        parent_start[start] = None
        parent_goal: ParentMap = dict()
        parent_goal[goal] = None
        visited_start: VisitedSet = {start}
        visited_goal: VisitedSet = {goal}

        # Emitir estado inicial
        yield {
            'current': start.coord,
            'action': 'visiting_start',
            'modified_cells': [start],
        }
        yield {
            'current': goal.coord,
            'action': 'visiting_goal',
            'modified_cells': [goal],
        }

        while queue_start and queue_goal:
            # Verificar si se encontró el punto de encuentro
            for visited in visited_start:
                if visited in visited_goal:
                    path = self.reconstruct_path(
                        parent_start, parent_goal, visited
                    )
                    self.reconstructed_path = path

                    # Limpiar todas las celdas visitadas (volver a negro)
                    all_visited = list(visited_start.union(visited_goal))
                    yield {
                        'current': visited.coord,
                        'action': 'clear_visited',
                        'modified_cells': all_visited,
                    }

                    # Luego mostrar solo el camino de solución
                    yield {
                        'current': visited.coord,
                        'action': 'solution_found',
                        'modified_cells': path,
                    }
                    return

            # Expandir desde el inicio
            node_start = queue_start.popleft()

            new_neighbors = []
            for neighbor in node_start.get_accessible_neighbors().values():
                if neighbor not in visited_start:
                    queue_start.append(neighbor)
                    visited_start.add(neighbor)
                    parent_start[neighbor] = node_start
                    new_neighbors.append(neighbor)

            # Si añadimos vecinos, emitir evento para pintarlos
            if new_neighbors:
                yield {
                    'current': node_start.coord,
                    'action': 'visiting_start',
                    'modified_cells': new_neighbors,
                }

            # Expandir desde el objetivo
            node_goal = queue_goal.popleft()

            new_neighbors = []
            for neighbor in node_goal.get_accessible_neighbors().values():
                if neighbor not in visited_goal:
                    queue_goal.append(neighbor)
                    visited_goal.add(neighbor)
                    parent_goal[neighbor] = node_goal
                    new_neighbors.append(neighbor)

            if new_neighbors:
                yield {
                    'current': node_goal.coord,
                    'action': 'visiting_goal',
                    'modified_cells': new_neighbors,
                }

        # No se encontró solución
        yield {
            'current': None,
            'action': 'no_solution',
            'modified_cells': [],
        }

    @staticmethod
    def reconstruct_path(path_start: ParentMap,
                         path_goal: ParentMap,
                         meeting_node: Cell) -> List[Cell]:
        start_half: List[Cell] = []
        cur: Optional[Cell] = meeting_node
        while cur is not None:
            start_half.append(cur)
            cur = path_start[cur]
        start_half.reverse()

        goal_half: List[Cell] = []
        cur = path_goal[meeting_node]
        while cur is not None:
            goal_half.append(cur)
            cur = path_goal[cur]

        return start_half + goal_half
