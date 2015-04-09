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
        self.win = params[3]
        self.element_init()

    def element_init(self):
        """
        Initializes all UI elements
        """
        self.background = PictureBox(0, 0, pygame.image.load("assets/background.jpg").convert())

        # static element init
        self.static_elements=[]
        if self.win:
            self.static_elements.append(TextBox(40, self.level_name.rstrip() + " Cleared!"))
        else :
            self.static_elements.append(TextBox(40, "You guys lost to " + self.level_name.rstrip()))

        if not self.next_level or not self.win:
            num_buttons = 2
            button_width = 450
            button_height = 75
            button_x = (self.width - num_buttons * button_width - (num_buttons - 1) * button_width * 0.1) / 2
            button_y = self.height * 0.78
            self.buttons = RadioButtons(button_x, button_y, button_width, button_height, 1, self.players)
            self.buttons.x_spacing = button_width * 0.1
            if self.level_name == "Legacy Mode":
                self.buttons.add_radio_button((1, "level_select", ["legacy_game"]), "lets go again dad")
            else:
                self.buttons.add_radio_button((1, "level_select", ["main_game"]), "lets go again dad")
            self.buttons.add_radio_button((1, "main_menu", []), "main menu")

        self.static_elements[0].x = (self.width - self.static_elements[0].get_dimensions()[0]) / 2
        self.static_elements[0].y = self.height * 0.08
        self.static_elements.append(TextBox(20, "Back"))
        self.static_elements[1].x = self.width - self.static_elements[1].get_dimensions()[0] - 60
        self.static_elements[1].y = self.height - self.static_elements[1].get_dimensions()[1]*1.7
        self.static_elements.append(PictureBox(self.static_elements[1].x + self.static_elements[1].get_dimensions()[0] + 5, self.height - 53, \
                                    pygame.transform.scale(pygame.image.load("assets/icons/PS4_Circle.png").convert_alpha(), (45, 45))))
        self.static_elements.append(TextBox(20, "Select"))
        self.static_elements[3].x = self.static_elements[1].x - self.static_elements[2].get_dimensions()[0] - 60
        self.static_elements[3].y = self.height - self.static_elements[3].get_dimensions()[1]*1.7  
        self.static_elements.append(PictureBox(self.static_elements[3].x + self.static_elements[3].get_dimensions()[0] + 5, self.height - 53, \
                            pygame.transform.scale(pygame.image.load("assets/icons/PS4_Cross.png").convert_alpha(), (45, 45))))

        score_sorted_players = self.players[:]
        score_sorted_players.sort(key=lambda x:x.score, reverse=True)

        self.selectors = []
        if self.next_level == None or self.win == False:
            clear_status_functionality = False
        else:
            clear_status_functionality = True

        clear_status_x = self.width * 0.1
        clear_status_y = self.height * 0.23
        clear_status_width = self.width * 0.8
        clear_status_height = self.height * 0.08
        y_spacing = clear_status_height * 0.2

        for player in enumerate(score_sorted_players):
            self.selectors.append(CharacterClearStatus(clear_status_x, clear_status_y + player[0] * (y_spacing + clear_status_height), \
                                                            clear_status_width, clear_status_height, player[1], clear_status_functionality))
    def update(self, dt):
        if self.next_level != None and self.win == True:
            locked_players = []

            for selector in self.selectors:
                update_status = selector.update()
                if update_status == True:
                    locked_players.append(selector.player)

            if self.players[0] in locked_players and self.players[0].get_debounced_input(5):
                if self.next_level != None:
                    return (1, "main_game", [locked_players, "levels/" + self.next_level])
        else:
            self.buttons.update()
            if self.players[0].get_debounced_input(5):
                return self.buttons.selected_button.event

        if self.players[0].get_debounced_input(6):
            return (0, "pause_menu", ["wait im not even"])

        return True

    def draw(self, screen, clock=None):
        screen.fill((255, 255, 255))
        self.background.draw(screen)
        if self.next_level == None or self.win == False:
            self.buttons.draw(screen)
        for element in self.static_elements:
            element.draw(screen)
        for selector in self.selectors:
            selector.draw(screen)

interfaces.interface_types["level_clear"] = Level_Clear