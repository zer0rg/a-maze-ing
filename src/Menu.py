"""Menu module for interactive user interface."""

import os
from enum import Enum

from src.Config import Config


class ExecOptions(Enum):
    """Enumeration of execution options."""

    GEN_MAZE_WITH_RENDER = 1
    GEN_MAZE_NO_RENDER = 2
    SHOW_SOLUTION_RENDER = 3
    SHOW_SOLUTION_NO_RENDER = 4
    CHANGE_COLOR = 5
    EXIT = 6
    HIDE_SOLVE_PATH = 7


class RenderOptions(Enum):
    """Enumeration of render options."""

    GENERATION = (0, "generate")
    SOLUTION = (1, "show the solution path")


class BackException(Exception):
    """Exception raised to return to main menu."""

    pass


class MenuPrintable(Enum):
    """Enumeration of printable menu strings."""

    MAIN_MENU = """1. New Maze
2. Show the solution path
3. Change walls color
4. Exit"""

    SOLVED_MENU = """1. New Maze
2. Hide the solution path
3. Change walls color
4. Exit"""

    LOGO = """
    █████╗       ███╗   ███╗ █████╗ ██████  ███████╗      \
██╗███╗   ██╗ ██████╗
   ██╔══██╗      ████╗ ████║██╔══██╗╚══███╔╝██╔════╝      \
██║████╗  ██║██╔════╝
   ███████║█████╗██╔████╔██║███████║  ███╔╝ █████╗  █████╗\
██║██╔██╗ ██║██║  ███╗
   ██╔══██║╚════╝██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  ╚════╝\
██║██║╚██╗██║██║   ██║
   ██║  ██║      ██║ ╚═╝ ██║██║  ██║███████╗███████╗      \
██║██║ ╚████║╚██████╔╝
   ╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝      \
╚═╝╚═╝  ╚═══╝ ╚═════╝
"""


class Menu:
    """Interactive menu for the maze application."""

    def __init__(
                self,
                config: Config
                 ):
        """Initialize the menu with configuration settings."""
        self.config = config
        self.status: str = ""
        self.generated: bool = False
        self.print_header()

    def init_menu(self,
                  status: str = "",
                  generated: bool = False,
                  solved: bool = False
                  ) -> ExecOptions:
        """Initialize and display the main menu."""
        self.status = status
        self.generated = generated
        self.print_header()
        if not generated:
            return self.ask_render_option(RenderOptions.GENERATION)
        if not solved:
            print(MenuPrintable.MAIN_MENU.value)
        if solved:
            print(MenuPrintable.SOLVED_MENU.value)
        print()
        try:
            selection = int(input("Select an option => "))
            if selection == 1:
                return self.ask_render_option(RenderOptions.GENERATION)
            elif selection == 2 and generated and not solved:
                return self.ask_render_option(RenderOptions.SOLUTION)
            elif selection == 2 and generated and solved:
                return ExecOptions.HIDE_SOLVE_PATH
            elif selection == 3 and generated:
                return ExecOptions.CHANGE_COLOR
            elif selection == 4 and generated:
                return ExecOptions.EXIT
            else:
                raise ValueError("Invalid option selected")
        except BackException:
            return self.init_menu("Going back to main menu...", generated)
        except ValueError as e:
            return self.init_menu(f"Error ex: ´{str(e)}", generated)

    def print_header(self) -> None:
        """Clear screen and print the application header."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(MenuPrintable.LOGO.value)
        print("\t\tWith <3 by amarcill & rgerman-\n")
        print("Generation configuration:")
        print(f"Width: {self.config.width} | \
        Height: {self.config.height} | \
        Entry: {self.config.entry} | \
        Exit: {self.config.exit} | \
        Perfect: {self.config.perfect}")
        if self.status != "":
            print(f"\nStatus\t=>\t{self.status}")
        print()

    def ask_render_option(self,
                          render_option: RenderOptions
                          ) -> ExecOptions:
        """Ask user for render option selection."""
        is_generate_option: bool = (
                render_option is RenderOptions.GENERATION)
        render_option_string = render_option.value[1]
        self.status = "Select render option for " + render_option_string
        self.print_header()
        print(f"How do you want to {render_option_string}?\n")
        print("1. Animated render (Will take longer)")
        print("2. Static render")
        if self.generated:
            print("3. Back to main menu")
        print()
        try:
            selection = int(input("Select an option => "))
            if is_generate_option:
                if selection == 1:
                    return ExecOptions.GEN_MAZE_WITH_RENDER
                elif selection == 2:
                    return ExecOptions.GEN_MAZE_NO_RENDER
                elif selection == 3 and self.generated:
                    raise BackException()
                else:
                    raise ValueError("Invalid option selected")
            else:
                if selection == 1:
                    return ExecOptions.SHOW_SOLUTION_RENDER
                elif selection == 2:
                    return ExecOptions.SHOW_SOLUTION_NO_RENDER
                elif selection == 3 and self.generated:
                    raise BackException()
                else:
                    raise ValueError("Invalid option selected")
        except ValueError as e:
            self.status = "Error: " + str(e)
            return self.ask_render_option(render_option)

    @staticmethod
    def ask_color_code() -> int | None:
        """Prompt user for a hexadecimal color code."""
        try:
            color: int = int(input("\nWrite the HEX color code => "), 16)
        except ValueError:
            print("Color must be valid hexadecimal (0xFFFFFF) or integer")
            return None

        return color
