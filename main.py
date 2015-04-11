from gui import *

SCREEN_SIZE = (1280, 720)

main_gui = GUI(*SCREEN_SIZE)
main_gui.set_caption("enthalPy")
main_gui.set_icon(pygame.image.load("assets/icons/PS4_Triangle.png").convert_alpha())

menu = interfaces.interface_types["main_menu"](main_gui.players, SCREEN_SIZE[0], SCREEN_SIZE[1], [])

# add main menu to the gui's interfaces and run the gui to launch the game
main_gui.add_interface(menu)
main_gui.run()