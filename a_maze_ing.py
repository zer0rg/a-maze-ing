import sys
from typing import List
sys.path.append("./src")
from MazeConfig import MazeConfig
from MazeRenderer import MazeRenderer
from MazeGenerator import MazeGenerator
from InteractiveMenu import InteractiveMenu

class Maze:
    def __init__(self):
        self.config : MazeConfig = MazeConfig()
        self.renderer: MazeRenderer = MazeRenderer()
        self.generator : MazeGenerator = MazeGenerator(self.config)
        self.menu : InteractiveMenu = InteractiveMenu()
        try:
            self.board : List[List[int]] = self.generator.generate()
            self.renderer.render(self.board)
            # Propagar cualquier tipo de Error en el generador y renderer!!
        except Exception:
            print("There was an error generating the maze...")


if __name__ == "__main__":
    maze : Maze = Maze()