import pygame
import interfaces
import time
from interfaces.interface import Interface
from drawing import *
from elements import *

class Level_Select(Interface):
    def __init__(self, players, width, height, params):
        super().__init__(players, width, height, params)
        self.element_init()
        time.sleep(0.15) # button debounce

    def element_init(self):
        """
        Initializes all UI elements
        """
        self.buttons = []
        # static element init
        self.static_elements=[]
        self.static_elements.append(TextBox("Roboto", 40, "select level"))
        self.static_elements[0].x = (self.width - self.static_elements[0].get_dimensions()[0]) / 2
        self.static_elements[0].y = self.height * 0.07

        self.selectors = []
        x_spacing = 20

        selector_width = min(self.width * 0.18, (self.width - (len(self.players) - 1) * x_spacing))
        selector_height = self.height * 0.4
        selector_x = (self.width - len(self.players) * selector_width - (len(self.players) - 1) * x_spacing) / 2
        selector_y = self.height * 0.2

        for player in enumerate(self.players):
            self.selectors.append(CharacterSelect(selector_x + player[0] * (x_spacing + selector_width), \
                                 selector_y, selector_width, selector_height, player[1], player[0] + 1))

    def update(self, dt):
        not_joined = False
        locked = False
        locked_players = []

        for selector in self.selectors:
            update_status = selector.update()
            if selector.player == self.players[0] and update_status[1] == True:
                locked = True
                locked_players.append(selector.player)
                selector.player.color = CharacterSelect.COLORS[selector.color_selection]
            elif selector.player == self.players[0] and update_status[0] == 0:
                not_joined = True
            elif update_status == True:
                locked_players.append(selector.player)
                selector.player.color = CharacterSelect.COLORS[selector.color_selection]

        if locked and self.players[0].get_input()[5]:
            return (1, "main_game", [locked_players])
        elif not_joined and self.players[0].get_input()[7]:
            return (1, "main_menu", [])

        return True

    def draw(self, screen, clock=None):
        screen.fill((255, 255, 255))
        for button in self.buttons:
            button.draw(screen)
        for element in self.static_elements:
            element.draw(screen)
        for selector in self.selectors:
            selector.draw(screen)

interfaces.interface_types["level_select"] = Level_Select