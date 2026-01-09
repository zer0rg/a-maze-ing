import sys
sys.path.append("./src")
from MazeConfig import MazeConfig
from MazeRenderer import MazeRenderer
from MazeGenerator import MazeGenerator

class Maze:
    def __init__(self):
        self.board = []
        self.config : MazeConfig = MazeConfig()
        self.renderer: MazeRenderer = MazeRenderer()
        self.generator : MazeGenerator = MazeGenerator(self.config)
        

if __name__ == "__main__":
    maze : Maze = Maze()