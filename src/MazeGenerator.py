import sys
sys.path.append("./src")
from MazeConfig import MazeConfig
from typing import List, Tuple

class MazeGenerator:
    def __init__(self, config : MazeConfig):
        self.width = config.width
        self.height = config.height
        self.perfect = config.perfect
        self.entry = config.entry
        self.exit = config.exit

    def generate(self)-> List[List[int]]:
        pass
#       Podemos generar un laberinto perfecto con backtracking recursivo,
#       y si PERFECT=FALSE añadimos caminos extra de alguna manera???