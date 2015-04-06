import pygame
import interfaces
from interfaces.interface import Interface
from drawing import *

class Main_Menu(Interface):
    def __init__(self, players, width, height):
        super().__init__(players, width, height)

    def update(self, screen, dt):
        if self.players:
            if self.players[0].get_input()[5]:
            	return (False, "main_game")
                # self.gui.interfaces.remove(self)
                # self.gui.interfaces.append(Main_Game(self.gui))
            if self.players[0].get_input()[4]:
            	return (False, None)

        return True

    def draw(self, screen):
        screen.fill((255, 255, 255))

interfaces.interface_types["main_menu"] = Main_Menu