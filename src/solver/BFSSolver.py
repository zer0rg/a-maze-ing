import queue
from collections import deque
from self_typing import MazeBoard
from solver.MazeSolver import MazeSolver

from MazeUtilities import MazeUtilities


class BFSSolver(MazeSolver):

    def __init__(self, board: MazeBoard, entry, exit):
        super().__init__(board, entry, exit)

    def solve(self):
        start, goal = self.entry, self.exit
        queue = deque([start])
        visited = {start}
        parent = dict()
        parent[start] = None
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


if __name__ == '__main__':
    maze_board: MazeBoard = {
        (0, 0): 13,
        (0, 1): 3,
        (0, 2): 15,
        (1, 0): 3,
        (1, 1): 10,
        (1, 2): 12,
        (2, 0): 15,
        (2, 1): 12,
        (2, 2): 7,
    }

    MazeSolver = BFSSolver(maze_board, (0, 0), (2,2))
    print(MazeSolver.solve())