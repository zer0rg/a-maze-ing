import os

class InteractiveMenu:

    def __init__(self):
        print("""
    █████╗       ███╗   ███╗ █████╗ ██████\ ███████╗      ██╗███╗   ██╗ ██████╗ 
   ██╔══██╗      ████╗ ████║██╔══██╗╚══███╔╝██╔════╝      ██║████╗  ██║██╔════╝ 
   ███████║█████╗██╔████╔██║███████║  ███╔╝ █████╗  █████╗██║██╔██╗ ██║██║  ███╗
   ██╔══██║╚════╝██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  ╚════╝██║██║╚██╗██║██║   ██║
   ██║  ██║      ██║ ╚═╝ ██║██║  ██║███████╗███████╗      ██║██║ ╚████║╚██████╔╝
   ╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝      ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
    """)
        print("         With <3 by amarcill & rgerman-\n")

#       Clase para manejar el menu interactivo del programa
    def init_menu(self):
        print("\nSelect an option:")
        print("1. Generate a new maze")
        print("2. Show the solution path")
        print("3. Exit")
        try:
            selection = int(input("=> "))
        except Exception:
            print("Error: Only integers are admitted")
            return self.init_menu()
        if selection:
            try:
                option = int(selection)
            except ValueError:
                print("Please enter a valid number")