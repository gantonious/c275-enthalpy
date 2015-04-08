import pygame
import interfaces
from interfaces.interface import Interface
from drawing import *
from elements import *

class Main_Menu(Interface):
    def __init__(self, players, width, height, params):
        super().__init__(players, width, height, params)
        self.element_init()

    def element_init(self):
        """
        Initializes all UI elements
        """
        # button init
        self.buttons = []
        num_buttons = 2
        button_width = 500
        button_height = 75
        y_spacing = button_height * 0.25

        button_x = (self.width - button_width) / 2
        button_y = (self.height - num_buttons * button_height - (num_buttons - 1) * y_spacing) / 2
        self.buttons.append(Button(button_x, button_y, button_width, button_height, "level_select", "play"))
        self.buttons.append(Button(button_x, button_y + y_spacing + button_height, button_width, button_height, None, "exit"))
        self.buttons[0].selected = 1
        self.selected_button = self.buttons[0]

        # static element init
        self.static_elements=[]
        self.static_elements.append(TextBox(40, "Welcome to EnthalPy"))
        self.static_elements[0].x = (self.width - self.static_elements[0].get_dimensions()[0]) / 2
        self.static_elements[0].y = self.height * 0.2
        self.static_elements.append(TextBox(20, "Select"))
        self.static_elements[1].x = self.width - self.static_elements[1].get_dimensions()[0]*1.5
        self.static_elements[1].y = self.height * 0.94

    def update(self, dt):
        if self.players:
            if self.players[0].get_input()[3] < -self.threshold or self.players[0].get_input()[1] < -self.threshold:
                self.buttons[0].selected = 1
                self.buttons[1].selected = 0
                self.selected_button = self.buttons[0]
            elif self.players[0].get_input()[3] > self.threshold or self.players[0].get_input()[1] > self.threshold:
                self.buttons[0].selected = 0
                self.buttons[1].selected = 1
                self.selected_button = self.buttons[1]

            if self.players[0].get_debounced_input(5):
                return (1, self.selected_button.event, [])

        return True

    def draw(self, screen, clock=None):
        screen.fill((255, 255, 255))
        for button in self.buttons:
            button.draw(screen)
        for element in self.static_elements:
            element.draw(screen)

interfaces.interface_types["main_menu"] = Main_Menu