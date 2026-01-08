import sys
sys.path.append("./src")
from MazeConfig import MazeConfig

class Maze:
    def __init__(self):
        self.config = MazeConfig()

if __name__ == "__main__":
    maze = Maze()