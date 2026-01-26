#!/usr/bin/python3
from src import MazeConfig, MazeGenerator, InteractiveMenu, MazeRenderer
from src.solver.BFSSolver import BFSSolver
from src import OutputFileHandler
from self_typing import MazeBoard
import sys


class Maze:

    def __init__(self, config_file):
        self.config: MazeConfig = MazeConfig(config_file)
        self.renderer: MazeRenderer = MazeRenderer(self.config.width * 10,
                                                   self.config.height * 10)
        self.generator: MazeGenerator = MazeGenerator(self.config)
        self.menu: InteractiveMenu = InteractiveMenu()
        try:
            # Iniciar el renderer en thread separado
            self.renderer.start_loop()
            
            # Renderizar el maze inicial vacío
            self.renderer.render(self.generator.maze)
            
            # Configurar animación de generación
            animation = self.generator.generate_step_by_step()
            self.renderer.set_animation(animation)
            # Esperar a que se cierre la ventana
            self.renderer.wait_until_closed()
            self.renderer.destroy()
            
            # TODO: Menú interactivo
            # self.menu.init_menu()
            #self.solver = BFSSolver(self.board,
            #                        self.config.entry, self.config.exit)
            #self.solver.solve()
            #OutputFileHandler.save_file(self.config.output_file, self.board)
        except Exception as e:
            print(f"There was an error generating the maze... : {e}")
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

    try:
        maze = Maze(config_file)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)
