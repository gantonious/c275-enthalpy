import sys
from interfaces.main_menu import Main_Menu
from gui import *

argv = sys.argv[1:]
if len(argv) > 1:
    SCREEN_SIZE = (int(argv[0]), int(argv[1]))
else:
    SCREEN_SIZE = (1280, 720)


main_gui = GUI(*SCREEN_SIZE)
main_gui.set_caption("enthalPy")

menu = Main_Menu(main_gui)

main_gui.add_interface(menu)
main_gui.run()