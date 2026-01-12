from collections import deque
from self_typing.maze import MazeBoard
from src.solver.MazeSolver import MazeSolver
from src.MazeUtilities import MazeUtilities


class BFSSolver(MazeSolver):

    def __init__(self, board: MazeBoard, entry, exit):
        super().__init__(board, entry, exit)

    def solve(self):
        queue = deque([self.entry])
        visited = {self.entry}
        parent = dict()
        parent[self.entry] = None
        while queue:
            node = queue.popleft()
            if node == self.exit:
                return self.reconstruct_path(parent)
            for neighbor in MazeUtilities.get_neighbors(node, self.board):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = node
        return []

    def reconstruct_path(self, path: dict):
        steps = [self.exit]
        child = path[self.exit]
        while child is not None:
            steps.append(child)
            child = path[child]
        return steps
