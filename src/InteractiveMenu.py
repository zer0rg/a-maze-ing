import os
import sys


class InteractiveMenu:

    def __init__(
                self
                 ):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_logo()

#       Clase para manejar el menu interactivo del programa
    def init_menu(self, generation_callback):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_logo()
        print("\nSelect an option:")
        print("1. Generate a new maze")
        print("2. Show the solution path")
        print("3. Exit")
        try:
            selection = int(input("=> "))
            print()
        except Exception:
            print("Error: Only integers are admitted")
            return self.init_menu(generation_callback)
        if selection:
            try:
                option = int(selection)
                if option == 1:
                    generation_callback()
                if option == 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    sys.exit(0)
            except ValueError:
                print("Please enter a valid number")

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
