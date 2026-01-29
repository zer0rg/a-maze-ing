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
        print("\nSelect an option:")
        print("1. Generate a new maze")
        print("2. Show the solution path")
        print("3. Change background color")
        print("4. Exit")
        try:
            return int(input("=> "))
        except Exception:
            print("Error: Only integers are admitted")
            return self.init_menu()
        

    def print_config(self):
        print(f"Width: {self.config.width} \
Height: {self.config.height} Perfect: {self.config.perfect}")

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
