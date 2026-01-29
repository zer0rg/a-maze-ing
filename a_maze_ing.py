#!/usr/bin/python3
from src import MazeConfig, MazeGenerator, InteractiveMenu, MazeRenderer, OutputFileHandler
from src.solver.BFSSolver import BFSSolver
import sys
import os


class Main:

    def __init__(self, config_file):
        # Parseo de archivo configuracion en objeto config
        self.config: MazeConfig = MazeConfig(config_file)

        # Calcular tamaño de ventana para celdas de ~20 píxeles
        window_width = min(self.config.width * 20, 1920)
        window_height = min(self.config.height * 20, 1080)

        # Instanciar clases principales
        self.renderer: MazeRenderer = MazeRenderer(window_width, window_height)
        self.generator: MazeGenerator = MazeGenerator(self.config)
        self.solver: BFSSolver = BFSSolver(
                                            self.generator.maze,
                                            self.config.entry,
                                            self.config.exit)
        self.menu: InteractiveMenu = InteractiveMenu(self.config)
        # Generacion y renderizado del primer laberinto y inicio del menu
        self.start_generation()

    def exec_result(self, selection: int):
        if selection:
            try:
                option = int(selection)
                if option == 1:
                    self.start_generation()
                elif option == 2:
                    # TODO
                    # self.solver.solve()
                    self.main_menu()
                elif option == 3:
                    # Cambiar color (automáticamente redibuja y sincroniza)
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
        self.renderer.set_background_color(select)
        self.renderer.set_visited_color(select)
        self.renderer.sync()
        self.main_menu()

    def main_menu(self):
        result: int = self.menu.init_menu()
        self.exec_result(result)

    def start_generation(self) -> None:
        try:
            self.generator.maze = self.generator._initialize_board()
            generation = self.generator.generate_step_by_step()
            self.renderer.initialize_generation(self.generator.maze,
                                                generation)
            self.renderer.run()
            OutputFileHandler().save_file(self.config.output_file,
                                          self.generator.maze)
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
