import pygame
import interfaces
from interfaces.interface import Interface
from drawing import *
from elements import *

class Pause_Menu(Interface):
    def __init__(self, players, width, height, params):
        super().__init__(players, width, height, params)
        self.level_name = params[0]
        self.element_init()

    def element_init(self):
        """
        Initializes all UI elements
        """
        # button init
        num_buttons = 2
        button_width = 450
        button_height = 75
        button_x = (self.width - button_width) / 2
        button_y = (self.height - num_buttons * button_height - (num_buttons - 1) * button_height * 0.25) / 2

        self.buttons = RadioButtons(button_x, button_y, button_width, button_height, self.players)

        self.buttons.add_radio_button((1, None, []), "resume")
        self.buttons.add_radio_button((2, "main_menu", []), "return to menu")

        # static element init
        self.static_elements=[]
        self.static_elements.append(TextBox(40, "paused"))
        self.static_elements[0].x = (self.width - self.static_elements[0].get_dimensions()[0]) / 2
        self.static_elements[0].y = self.height * 0.2
        self.static_elements.append(TextBox(25, "playing " + self.level_name.rstrip()))
        self.static_elements[1].x = (self.width - self.static_elements[1].get_dimensions()[0]) / 2
        self.static_elements[1].y = self.height * 0.29


    def update(self, dt):
        if self.players:
            self.buttons.update()

            if self.players[0].get_debounced_input(5):
                return self.buttons.selected_button.event
            elif self.players[0].get_debounced_input(7):
                return (1, None, [])

        return True

    def draw(self, screen, clock=None):
        pygame.draw.rect(screen, (255, 255, 255), (self.width * 0.2, self.height * 0.16, self.width * 0.6, self.height * 0.55))
        pygame.draw.rect(screen, (0, 0, 0), (self.width * 0.2, self.height * 0.16, self.width * 0.6, self.height * 0.55), 2)
        self.buttons.draw(screen)
        for element in self.static_elements:
            element.draw(screen)

interfaces.interface_types["pause_menu"] = Pause_Menu