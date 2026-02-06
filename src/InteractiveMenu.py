import os
import sys
from src.MazeConfig import MazeConfig
import time

class InteractiveMenu:

    def __init__(
                self,
                config: MazeConfig
                 ):
        self.config = config
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_logo()
        self.print_config()

#       Clase para manejar el menu interactivo del programa
    def init_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_logo()
        self.print_config()
        print()
        print("1. New Maze")
        print("2. Show the solution path")
        print("3. Change background color")
        print("4. Exit")
        print()
        try:
            return int(input("Select an option => "))
        except Exception:
            print("Error: Only integers are admitted")
            return self.init_menu()
    def ask_color_code(self) -> int | None:
        try:
            color: int = int(input("\nWrite the HEX color code => "))
        except Exception:
            print("Color must be valid hexadecimal (0xFFFFFF) or integer")
            return None
        
        return color

    def print_config(self):
        print("Generation configuration:")
        print(f"Width: {self.config.width} | \
Height: {self.config.height} | \
Entry: {self.config.entry} | \
Exit: {self.config.exit} | \
Perfect: {self.config.perfect}")

    def print_logo(self):
        print("""
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
    """)
        print("\t\tWith <3 by amarcill & rgerman-\n")
