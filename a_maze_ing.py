#!/usr/bin/python3
from src.Menu import ExecOptions
from src import Config, Generator, Menu, Renderer
from src import OutputFileHandler
from src import Solver
import sys
import os


class Main:

    def __init__(self, config_file):
        # Parseo de archivo configuracion en objeto config
        self.config: Config = Config(config_file)
        self.generator: Generator = Generator(self.config)
        self.renderer: Renderer = Renderer(self.config,
                                           self.generator)
        self.menu: Menu = Menu(self.config)
        self.solver: Solver = Solver(
            self.generator.maze,
            self.config.entry,
            self.config.exit)
        self.generated: bool = False
        self.main_menu("Welcome to A-Maze-Ing!", self.generated)

    def exec_result(self, selection: ExecOptions):
        if selection and isinstance(selection, ExecOptions):
            try:
                if selection is ExecOptions.GEN_MAZE_WITH_RENDER:
                    self.menu.print_header()
                    self.start_generation(ExecOptions.GEN_MAZE_WITH_RENDER)
                elif selection is ExecOptions.GEN_MAZE_NO_RENDER:
                    self.menu.print_header()
                    self.start_generation(ExecOptions.GEN_MAZE_NO_RENDER)
                elif selection is ExecOptions.SHOW_SOLUTION_RENDER:
                    if self.generated:
                        self.menu.print_header()
                        self.start_solving(ExecOptions.SHOW_SOLUTION_RENDER)
                    else:
                        self.main_menu("Error: Maze must be generated first",
                                       self.generated)
                elif selection is ExecOptions.SHOW_SOLUTION_NO_RENDER:
                    if self.generated:
                        self.menu.print_header()
                        self.start_solving(ExecOptions.SHOW_SOLUTION_NO_RENDER)
                    else:
                        self.main_menu("Error: Maze must be generated first",
                                       self.generated)
                elif selection is ExecOptions.CHANGE_COLOR:
                    self.change_background_color()
                elif selection is ExecOptions.EXIT:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Exiting program...")
                    if hasattr(self, 'renderer'):
                        self.renderer.destroy()
                    sys.exit(0)
                else:
                    self.main_menu("Error: Invalid option selected",
                                   self.generated)
            except ValueError:
                self.main_menu("Error: Only integers are admitted",
                               self.generated)
            except Exception as error:
                self.main_menu(f"Unexpected error occurred: \
{error.__str__()}\n Report it pls! <3", self.generated)

    def change_background_color(self) -> None:
        select = self.menu.ask_color_code()
        if select is None:
            self.change_background_color()
        self.renderer.set_background_color(select)  # type: ignore
        self.renderer.set_visited_color(select)  # type: ignore
        self.renderer.sync()
        self.main_menu("Background color changed successfully!",
                       self.generated)

    def main_menu(self, status: str = "", generated: bool = False):
        result: ExecOptions = self.menu.init_menu(status, generated)
        self.exec_result(result)

    def start_generation(self, generation_type: ExecOptions) -> None:
        state = ""
        try:
            self.generated = False
            self.generator.initialize_board()
            if generation_type is ExecOptions.GEN_MAZE_WITH_RENDER:
                self.renderer.generation_complete = False
                self.renderer.initialize_rendered_generation()
                self.renderer.run()
                state = "Maze generated successfully with animation!"
            if generation_type is ExecOptions.GEN_MAZE_NO_RENDER:
                self.renderer.generation_complete = False
                self.generator.generate()
                self.renderer.draw_maze()
                self.renderer.sync()
                self.renderer.generation_complete = True
            if self.renderer.generation_complete:
                OutputFileHandler().save_file("maze.txt",
                                                        self.generator.maze,
                                                        self.config,
                                                        self.solver)
                self.generated = True
                state = f"Maze generated successfully!"
            else:
                self.generated = False
                state = "Maze generation was not completed!"
            self.main_menu(state,
                           self.generated)
        except Exception as e:
            self.generated = False
            print(f"Fatal error occurred: {e}")
            if hasattr(self, 'renderer'):
                self.renderer.destroy()

    def start_solving(self, solving_option: ExecOptions) -> None:
        try:
            if solving_option is ExecOptions.SHOW_SOLUTION_RENDER:
                # Resolver con animación paso a paso
                print("Solving maze with animation...")
                self.renderer.initialize_rendered_solving(self.solver.solve_step_by_step())
                self.renderer.run()

                # Guardar el path una vez completado
                if self.solver.reconstructed_path:
                    with open("solved_path.txt", "w") as f:
                        for cell in self.solver.reconstructed_path:
                            f.write(f"{cell.coord}\n")

            elif solving_option is ExecOptions.SHOW_SOLUTION_NO_RENDER:
                # Resolver sin animación y mostrar resultado final
                print("Solving maze without animation...")
                self.renderer.solving_generator = None
                solution = self.solver.solve()

                if solution:
                    self.renderer.draw_solution(solution)
                    self.renderer.sync()

                    # Guardar solución
                    with open("solved_path.txt", "w") as f:
                        for cell in solution:
                            f.write(f"{cell.coord}\n")
                else:
                    print("No solution found!")

            self.main_menu("Solving completed!", self.generated)

        except Exception as e:
            print(f"Fatal error occurred during solving: {e}")
            if hasattr(self, 'renderer'):
                self.renderer.destroy()

if __name__ == "__main__":
    try:
        Main(Config.get_config_file())
    except Exception as e:
        print(f"{e}")
        sys.exit(1)
