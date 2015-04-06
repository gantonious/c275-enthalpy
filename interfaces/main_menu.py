import pygame
import interfaces
from interfaces.interface import Interface
from drawing import *
from elements import *

class Main_Menu(Interface):
    def __init__(self, players, width, height):
        super().__init__(players, width, height)
        self.button_reset()

    def button_reset(self):
        """
        Resets buttons and initializes them
        """
        self.buttons = []
        self.buttons.append(Button(10, 10, 300, 50, "main_game", "play"))
        self.buttons.append(Button(10, 70, 300, 50, None, "exit"))
        self.buttons[0].selected = 1
        self.selected_button = self.buttons[0]

    def update(self, dt):
        if self.players:
            if self.players[0].get_input()[3] < -0.08 or self.players[0].get_input()[1] < -0.08:
                self.buttons[0].selected = 1
                self.buttons[1].selected = 0
                self.selected_button = self.buttons[0]
            elif self.players[0].get_input()[3] > 0.08 or self.players[0].get_input()[1] > 0.08:
                self.buttons[0].selected = 0
                self.buttons[1].selected = 1
                self.selected_button = self.buttons[1]

            if self.players[0].get_input()[5]:
                return (False, self.selected_button.event)

        return True

    def draw(self, screen, clock=None):
        screen.fill((255, 255, 255))
        for button in self.buttons:
            button.draw(screen)

interfaces.interface_types["main_menu"] = Main_Menu