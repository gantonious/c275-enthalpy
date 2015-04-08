import pygame
import interfaces
from interfaces.interface import Interface
from drawing import *
from elements import *

class Level_Clear(Interface):
    def __init__(self, players, width, height, params):
        super().__init__(players, width, height, params)
        self.players = params[0]
        self.level_name = params[1]
        self.next_level = params[2]
        self.element_init()

    def element_init(self):
        """
        Initializes all UI elements
        """
        # button init
        self.buttons = []

        # static element init
        self.static_elements=[]
        self.static_elements.append(TextBox(40, "Level " + self.level_name.rstrip() + " Cleared!"))
        self.static_elements[0].x = (self.width - self.static_elements[0].get_dimensions()[0]) / 2
        self.static_elements[0].y = self.height * 0.08

        score_sorted_players = self.players
        score_sorted_players.sort(key=lambda x:x.score)

        clear_status_x = self.width * 0.1
        clear_status_y = self.height * 0.23
        clear_status_width = self.width * 0.8
        clear_status_height = self.height * 0.15
        y_spacing = clear_status_height * 0.2

        for player in enumerate(score_sorted_players):
            self.static_elements.append(CharacterClearStatus(clear_status_x, clear_status_y + player[0] * (y_spacing + clear_status_height), \
                                                            clear_status_width, clear_status_height, player[1], player[0] + 1))
    def update(self, dt):
        if self.players[0].get_debounced_input(5):
            if self.next_level != None:
                return (1, "main_game", [self.players, "levels/" + self.next_level])
            else:
                return (1, "main_menu", [])
            saver = Saver()
            saver.save(self.next_level)
            
        return True

    def draw(self, screen, clock=None):
        screen.fill((255, 255, 255))
        for button in self.buttons:
            button.draw(screen)
        for element in self.static_elements:
            element.draw(screen)   

interfaces.interface_types["level_clear"] = Level_Clear