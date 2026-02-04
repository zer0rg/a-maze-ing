from src.MazeGenerator import MazeGenerator
from src.MazeConfig import MazeConfig
from src.solver.BidirectionalBFSSolver import BidirectionalBFSSolver

if __name__ == "__main__":
    config_file = "config.txt"
    config = MazeConfig(config_file)
    generator = MazeGenerator(config)
    generator.generate_step_by_step()
    solver = BidirectionalBFSSolver(generator.maze, config.entry, config.exit)
    print(f"{generator.maze}")
    for cell in generator.maze.values():
        print(cell)
    path = solver.solve()
    print(f"Path found: {path}")
