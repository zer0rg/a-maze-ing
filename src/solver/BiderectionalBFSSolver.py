import queue
from collections import deque
from self_typing import MazeBoard
from solver.MazeSolver import MazeSolver

from MazeUtilities import MazeUtilities


class BidirectionalBFSSolver(MazeSolver):

    def __init__(self, board: MazeBoard, entry, exit):
        super().__init__(board, entry, exit)

    def solve(self):
        start, goal = self.entry, self.exit
        queue_start = deque([start])
        queue_goal = deque([goal])
        parent_start  = dict()
        parent_start[start] = None
        parent_goal = dict()
        parent_goal[goal] = None
        visited_start = {start}
        visited_goal = {goal}
        while queue_start and queue_goal:
            for visited in visited_start:
                if visited in visited_goal:
                    return self.reconstruct_path(parent_start, parent_goal, visited)
            node_start = queue_start.popleft()
            for neighbor in MazeUtilities.get_neighbors(node_start, self.board):
                if neighbor not in visited_start:
                    queue_start.append(neighbor)
                    visited_start.add(neighbor)
                    parent_start[neighbor] = node_start
            node_goal = queue_goal.popleft()
            for neighbor in MazeUtilities.get_neighbors(node_goal, self.board):
                if neighbor not in visited_goal:
                    queue_goal.append(neighbor)
                    visited_goal.add(neighbor)
                    parent_goal[neighbor] = node_goal
        return [parent_start, parent_goal]

    def reconstruct_path(self, path_start, path_goal, meeting_node):
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


if __name__ == '__main__':
    maze_board = {
        # Fila 0 (pared norte)
        (0, 0): 9,  # Norte + Oeste
        (0, 1): 1,
        (0, 2): 1,
        (0, 3): 1,
        (0, 4): 3,  # Norte + Este

        # Fila 1 (interior sin paredes)
        (1, 0): 8,  # Oeste
        (1, 1): 0,
        (1, 2): 0,
        (1, 3): 0,
        (1, 4): 2,  # Este

        # Fila 2 (interior sin paredes)
        (2, 0): 8,
        (2, 1): 0,
        (2, 2): 0,
        (2, 3): 0,
        (2, 4): 2,

        # Fila 3 (interior sin paredes)
        (3, 0): 8,
        (3, 1): 0,
        (3, 2): 0,
        (3, 3): 0,
        (3, 4): 2,

        # Fila 4 (pared sur)
        (4, 0): 12,  # Sur + Oeste
        (4, 1): 4,
        (4, 2): 2,
        (4, 3): 4,
        (4, 4): 6,  # Sur + Este
    }

    MazeSolver = BidirectionalBFSSolver(maze_board, (0, 0), (4,4))
    print(MazeSolver.solve())