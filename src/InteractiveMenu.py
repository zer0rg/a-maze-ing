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
        print("Select an option:")
        print("1. Generate a new maze")
        print("2. Show the solution path")
        print("3. Exit")
        selection = input(int("=>"))
        if selection:
            pass