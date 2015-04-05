import pygame, sys
from threading import Thread
from entities.individuals import *
from main_game import Main_Game
from quadtree import Quadtree
from gui import *
from loader import *
from textprint import TextPrint

argv = sys.argv[1:]
if len(argv) > 1:
    SCREEN_SIZE = (int(argv[0]), int(argv[1]))
else:
    SCREEN_SIZE = (1280, 720)


main_gui = GUI(*SCREEN_SIZE)
main_gui.set_caption("enthalPy")

main_game = Main_Game(main_gui)

main_gui.add_interface(main_game)
main_gui.run()