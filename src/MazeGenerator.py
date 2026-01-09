import sys
sys.path.append("./src")
from MazeConfig import MazeConfig
from typing import List, Dict, Tuple, TypeAlias

MazeCell : TypeAlias = Dict[str, bool]
#  {(x, y) : {'N': True, 'E': True, 'S': True, 'W': True}}
#  No se que tal te parece esta forma de representar cada celda,
#  ami me mola :)
MazeBoard : TypeAlias = Dict[Tuple[int, int], MazeCell]

class MazeGenerator:
   
    def __init__(self, config : MazeConfig):
        self.width = config.width
        self.height = config.height
        self.perfect = config.perfect
        self.entry = config.entry
        self.exit = config.exit
        self.output_file = config.output_file
        self.maze : MazeBoard = self._initialize_board()


    def generate(self)-> MazeBoard:
        pass
#       Podemos generar un laberinto perfecto con backtracking recursivo,
#       y si PERFECT=FALSE añadimos caminos extra de alguna manera???
        return self.maze
      

    def save_to_file(self):
        with open(self.output_file, "w") as output_file:
            pass


    def _initialize_board(self) -> MazeBoard:
        maze : MazeBoard = {}
        for y in range(self.height):
            for x in range(self.width):
                maze[(x, y)] = {'N': True, 'E': True, 'S': True, 'W': True}
        return maze
