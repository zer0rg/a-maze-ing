from collections import deque
from typing import MazeBoard
from solver.MazeSolver import MazeSolver
from MazeUtilities import MazeUtilities


class BFSSolver(MazeSolver):

    def __init__(self, board: MazeBoard, entry, exit):
        super().__init__(board, entry, exit)

    def solve(self):
        queue = deque([self.entry])
        visited = {self.entry}
        while queue:
            node = queue.popleft()
            if node == self.exit:
                print("Visited final node:", self.exit)
                return 0
            print("Visited: ", node)
            for neighbor in MazeUtilities.get_neighbors(node, self.board):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        print("Final node not reached:", self.exit)
        return -1
