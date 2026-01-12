from src.solver.BiderectionalBFSSolver import BidirectionalBFSSolver
from src.MazeUtilities import MazeUtilities
from self_typing.maze import NORTH, EAST, SOUTH, WEST

if __name__ == '__main__':
    maze_board = {(1, 1): 15, (2, 1): 15, (3, 1): 15, (4, 1): 15, (5, 1): 15, (1, 2): 15, (2, 2): 15, (3, 2): 15, (4, 2): 15, (5, 2): 15, (1, 3): 15, (2, 3): 15, (3, 3): 15, (4, 3): 15, (5, 3): 15, (1, 4): 15, (2, 4): 15, (3, 4): 15, (4, 4): 15, (5, 4): 15, (1, 5): 15, (2, 5): 15, (3, 5): 15, (4, 5): 15, (5, 5): 15}

    MazeSolver = BidirectionalBFSSolver(maze_board, (1, 1), (4, 4))
    print(MazeSolver.solve())
