from collections import deque
from typing import Dict, Set
from self_typing.maze import Coordinate, MazeBoard
from src.Cell import Cell
from src.solver.MazeSolver import MazeSolver


class BidirectionalBFSSolver(MazeSolver):

    def __init__(self, board: MazeBoard, entry: Coordinate, exit: Coordinate):
        super().__init__(board, entry, exit)
        self.reconstructed_path = None

    def solve(self):
        """
        Resuelve el laberinto usando BFS bidireccional de forma completa.
        Retorna el camino de solución o None si no existe.
        """
        print("\nSolving maze...")
        start = self.board.get(self.entry)
        goal = self.board.get(self.exit)
        queue_start = deque([start])
        queue_goal = deque([goal])
        parent_start: Dict[Cell, Cell] = dict()
        parent_start[start] = None
        parent_goal: Dict[Cell, Cell] = dict()
        parent_goal[goal] = None
        visited_start: Set[Cell] = {start}
        visited_goal: Set[Cell] = {goal}

        while queue_start and queue_goal:
            # Verificar si se encontró el punto de encuentro
            for visited in visited_start:
                if visited in visited_goal:
                    path = self.reconstruct_path(parent_start, parent_goal, visited)
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

    def solve_step_by_step(self):
        """
        Genera la solución paso a paso usando BFS bidireccional.
        Emite eventos para renderizar la exploración en tiempo real.
        Similar al generate_step_by_step del MazeGenerator.
        """
        print("\nSolving...")
        print("Press Q in the maze window to abort solving")

        start = self.board.get(self.entry)
        goal = self.board.get(self.exit)
        queue_start = deque([start])
        queue_goal = deque([goal])
        parent_start: Dict[Cell, Cell] = dict()
        parent_start[start] = None
        parent_goal: Dict[Cell, Cell] = dict()
        parent_goal[goal] = None
        visited_start: Set[Cell] = {start}
        visited_goal: Set[Cell] = {goal}

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
                    path = self.reconstruct_path(parent_start, parent_goal, visited)
                    self.reconstructed_path = path

                    # Primero limpiar todas las celdas visitadas (volver a negro)
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
    def reconstruct_path(path_start: Dict[Cell, Cell],
                         path_goal: Dict[Cell, Cell],
                         meeting_node: Cell):
        start_half = []
        cur = meeting_node
        while cur is not None:
            start_half.append(cur)
            cur = path_start[cur]
        start_half.reverse()

        goal_half = []
        cur = path_goal[meeting_node]
        while cur is not None:
            goal_half.append(cur)
            cur = path_goal[cur]

        return start_half + goal_half
