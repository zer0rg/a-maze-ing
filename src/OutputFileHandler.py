from self_typing.maze import MazeBoard
from src.MazeConfig import MazeConfig
from src.solver import BidirectionalBFSSolver


class OutputFileHandler:

    @staticmethod
    def save_file(file_name: str, maze: MazeBoard, config: MazeConfig, solver: BidirectionalBFSSolver) -> str:
        with open(file_name, "w") as file:
            for y in range(1, config.height + 1):
                for x in range(1, config.width + 1):
                    file.write(f"{format(maze[(x, y)].walls, 'X')}")
                    if x == config.width:
                        file.write("\n")
            file.write("\n\n")
            file.write(f"{config.entry[0]},{config.entry[1]}\n")
            file.write(f"{config.exit[0]},{config.exit[1]}\n")
            path = solver.solve()
            file.write(f"{len(path) if path else 0}\n")
            actual = None
            while path:
                actual = path.pop(0)
                next_cell = path[0] if path else None
                if next_cell is None:
                    break
                if actual.coord[0] < next_cell.coord[0]:
                    file.write("E\n")
                elif actual.coord[0] > next_cell.coord[0]:
                    file.write("W\n")
                elif actual.coord[1] < next_cell.coord[1]:
                    file.write("S\n")
                elif actual.coord[1] > next_cell.coord[1]:
                    file.write("N\n")
        return file_name
