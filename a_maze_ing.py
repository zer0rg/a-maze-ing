from MazeConfig import MazeConfig
from MazeRenderer import MazeRenderer
from MazeGenerator import MazeGenerator
from InteractiveMenu import InteractiveMenu
from typing import List
import sys
sys.path.append("./src")


class Maze:

    def __init__(self, config_file):
        self.config: MazeConfig = MazeConfig(config_file)
        self.renderer: MazeRenderer = MazeRenderer()
        self.generator: MazeGenerator = MazeGenerator(self.config)
        self.menu: InteractiveMenu = InteractiveMenu()
        try:
            self.board: List[List[int]] = self.generator.generate()
            self.renderer.render(self.board)
            # Propagar cualquier tipo de Error en el generador y renderer!!
        except Exception:
            print("There was an error generating the maze...")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments!")
        print("Usage: python a_maze_ing.py <config_file.txt>")
        sys.exit(1)

    config_file = sys.argv[1]

    if not config_file.endswith('.txt'):
        print("Error: Configuration file must be a .txt file!")
        print("Usage: python a_maze_ing.py <config_file.txt>")
        sys.exit(1)

    try:
        maze = Maze(config_file)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)
