#!/usr/bin/python3
from src import MazeConfig, MazeGenerator, InteractiveMenu, MazeRenderer
from src import OutputFileHandler
import sys
import os
import time


class Main:

    def __init__(self, config_file):
        # Parseo de archivo configuracion en objeto config
        self.config: MazeConfig = MazeConfig(config_file)

        MIN_CELL_SIZE = 10
        MAX_WINDOW_WIDTH = 1920
        MAX_WINDOW_HEIGHT = 900
        
        # Calcular el tamaño de celda que permita que todo quepa en pantalla
        cell_size_x = MAX_WINDOW_WIDTH // self.config.width
        cell_size_y = MAX_WINDOW_HEIGHT // self.config.height
        
        # Usar el menor tamaño para mantener proporciones
        cell_size = max(MIN_CELL_SIZE, min(cell_size_x, cell_size_y, 20))
        
        # Calcular dimensiones finales de la ventana
        window_width = min(self.config.width * cell_size, MAX_WINDOW_WIDTH)
        window_height = min(self.config.height * cell_size, MAX_WINDOW_HEIGHT)

        # Instanciar clases principales
        self.generator: MazeGenerator = MazeGenerator(self.config)
        self.renderer: MazeRenderer = MazeRenderer(window_width, window_height,
                                                   self.generator)
        self.menu: InteractiveMenu = InteractiveMenu(self.config)
        self.start_generation()

    def exec_result(self, selection: int):
        if selection:
            try:
                option = int(selection)
                if option == 1:
                    self.start_generation()
                elif option == 2:
                    # TODO
                    print("Comming soon!")
                    time.sleep(2)
                    self.main_menu()
                elif option == 3:
                    self.change_background_color()
                elif option == 4:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("See ya!")
                    sys.exit(0)
                else:
                    self.main_menu()
            except ValueError:
                self.main_menu()

    def change_background_color(self) -> None:
        select = self.menu.ask_color_code()
        if select is None:
            self.change_background_color()
        self.renderer.set_background_color(select)  # type: ignore
        self.renderer.set_visited_color(select)  # type: ignore
        self.renderer.sync()
        self.main_menu()

    def main_menu(self):
        result: int = self.menu.init_menu()
        self.exec_result(result)

    def start_generation(self) -> None:
        try:
            self.generator.maze = self.generator._initialize_board()
            self.renderer.initialize_rendered_generation()
            self.renderer.run()
            self.output = OutputFileHandler().save_file("maze.txt",
                                                        self.generator.maze,
                                                        self.config)
            self.main_menu()
        except Exception as e:
            print(f"Fatal error occurred: {e}")
            if hasattr(self, 'renderer'):
                self.renderer.destroy()


def get_config_file() -> str:
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments!")
        print("Usage: python a_maze_ing.py <config_file.txt>")
        sys.exit(1)

    config_file = sys.argv[1]

    if not config_file.endswith('.txt'):
        print("Error: Configuration file must be a .txt file!")
        print("Usage: python a_maze_ing.py <config_file.txt>")
        sys.exit(1)

    return config_file


if __name__ == "__main__":

    config_file = get_config_file()

    try:
        Main(config_file)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)
