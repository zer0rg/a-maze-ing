from collections import deque
from self_typing.maze import MazeBoard, Coordinate
from src.solver.MazeSolver import MazeSolver
from src.Cell import Cell


class BFSSolver(MazeSolver):

    def __init__(self, board: MazeBoard, entry: Coordinate, exit):
        super().__init__(board, entry, exit)

    def solve(self):
        entry_cell: Cell = self.board[self.entry]
        exit_cell: Cell = self.board[self.exit]
        queue = deque([entry_cell])
        parent = dict()
        parent[self.entry] = None
        while queue:
            actual_node: Cell = queue.popleft()
            if actual_node.coord == exit_cell.coord:
                return self.reconstruct_path(parent)
            for cell in self.board[(actual_node.coord)].neighbors:
                print(cell)
                #    if neighbor not in visited:
                #    queue.append(neighbor)
                #    visited.add(neighbor)
                #    parent[neighbor] = node
        return []

    def reconstruct_path(self, path: dict):
        steps = [self.exit]
        child = path[self.exit]
        while child is not None:
            steps.append(child)
            child = path[child]
        return steps
