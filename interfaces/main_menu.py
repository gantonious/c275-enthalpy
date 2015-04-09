import pygame
import interfaces
from interfaces.interface import Interface
from drawing import *
from elements import *

class Main_Menu(Interface):
    def __init__(self, players, width, height, params):
        super().__init__(players, width, height, params)
        self.element_init()
        pygame.mixer.stop()
        self.background_music = pygame.mixer.Sound(file = "assets/audio/title song.wav")
        self.background_music.play(loops=-1, fade_ms=2000)

    def element_init(self):
        """
        Initializes all UI elements
        """
        # button init
        num_buttons = 3
        button_width = 450
        button_height = 75
        button_x = (self.width - button_width) / 2
        button_y = (self.height - num_buttons * button_height - (num_buttons - 1) * button_height * 0.25) / 2

        self.buttons = RadioButtons(button_x, button_y, button_width, button_height, self.players)

        self.buttons.add_radio_button((1, "level_select", ["main_game"]), "cooperative play")
        self.buttons.add_radio_button((1, "level_select", ["legacy_game"]), "head to head")
        self.buttons.add_radio_button((1, None, []), "exit")

        self.background = PictureBox(0, 0, pygame.image.load("assets/background.jpg").convert())

        # static element init
        self.static_elements=[]
        self.static_elements.append(TextBox(40, "Welcome to EnthalPy"))
        self.static_elements[0].x = (self.width - self.static_elements[0].get_dimensions()[0]) / 2
        self.static_elements[0].y = self.height * 0.20
        self.static_elements[0].color = (255, 255, 255)
        self.static_elements.append(TextBox(20, "Select"))
        self.static_elements[1].x = self.width - self.static_elements[1].get_dimensions()[0] - 60
        self.static_elements[1].y = self.height - self.static_elements[1].get_dimensions()[1]*1.7
        self.static_elements.append(PictureBox(self.static_elements[1].x + self.static_elements[1].get_dimensions()[0] + 5, self.height - 53, \
                                    pygame.transform.scale(pygame.image.load("assets/icons/PS4_Cross.png").convert_alpha(), (45, 45))))

    def update(self, dt):
        if self.players:
            self.buttons.update()

            if self.players[0].get_debounced_input(5):
                return self.buttons.selected_button.event

        return True

    def draw(self, screen, clock=None):
        screen.fill((255, 255, 255))
        self.background.draw(screen)
        for element in self.static_elements:
            element.draw(screen)
        self.buttons.draw(screen)

interfaces.interface_types["main_menu"] = Main_Menu