from collections import deque
from self_typing.maze import MazeBoard
from src.solver.MazeSolver import MazeSolver
from src.MazeUtilities import MazeUtilities


class BidirectionalBFSSolver(MazeSolver):

    def __init__(self, board: MazeBoard, entry, exit):
        super().__init__(board, entry, exit)

    def solve(self):
        start, goal = self.entry, self.exit
        queue_start = deque([start])
        queue_goal = deque([goal])
        parent_start = dict()
        parent_start[start] = None
        parent_goal = dict()
        parent_goal[goal] = None
        visited_start = {start}
        visited_goal = {goal}
        while queue_start and queue_goal:
            for visited in visited_start:
                if visited in visited_goal:
                    self.reconstructed_path = self.reconstruct_path(parent_start, parent_goal,
                                                                    visited)
                    return self.reconstructed_path
            node_start = queue_start.popleft()
            for neighbor in MazeUtilities.get_neighbors(node_start,
                                                        self.board):
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
        return None

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

