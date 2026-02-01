from self_typing.maze import MazeBoard
from src.MazeConfig import MazeConfig
from src.solver.MazeSolver import MazeSolver


class OutputFileHandler:

    @staticmethod
    def save_file(file_name: str, maze: MazeBoard, config: MazeConfig) -> None:
        with open(file_name, "w") as file:
            for y in range(1, config.height + 1):
                for x in range(1, config.width + 1):
                    file.write(f"{format(maze[(x, y)].walls, 'X')}")
                    if x == config.width:
                        file.write("\n")
            file.write("\n\n")
            file.write(f"{config.entry[0]},{config.entry[1]}\n")
            file.write(f"{config.exit[0]},{config.exit[1]}\n")
