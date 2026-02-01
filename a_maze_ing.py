#!/usr/bin/python3
from src import MazeConfig, MazeGenerator, InteractiveMenu, MazeRenderer, OutputFileHandler
from src.solver.BiderectionalBFSSolver import BidirectionalBFSSolver
from src import OutputFileHandler
from self_typing import MazeBoard
import sys
import os
import time


class Main:

    def __init__(self, config_file):
        # Parseo de archivo configuracion en objeto config
        self.config: MazeConfig = MazeConfig(config_file)
        self.renderer: MazeRenderer = MazeRenderer(self.config.width * 10,
                                                   self.config.height * 10)
        self.generator: MazeGenerator = MazeGenerator(self.config)
        self.menu: InteractiveMenu = InteractiveMenu()
        try:
            self.board: MazeBoard = self.generator.generate()
            self.renderer.render(self.board)
            self.solver = BFSSolver(self.board,
                                    self.config.entry, self.config.exit)
            self.bidirectional_solver = BidirectionalBFSSolver(self.board,
                                                               self.config.entry, self.config.exit)
            print("RESULT: \n", self.solver.solve())
            OutputFileHandler.save_file(self.config.output_file, self.board)
            # Propagar cualquier tipo de Error en el generador y renderer!!
        except Exception as e:
            print(f"Fatal error occurred: {e}")
            if hasattr(self, 'renderer'):
                self.renderer.destroy()


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
