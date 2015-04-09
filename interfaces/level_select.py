import pygame
import interfaces
from interfaces.interface import Interface
from drawing import *
from elements import *
from loader import *

class Level_Select(Interface):
    def __init__(self, players, width, height, params):
        super().__init__(players, width, height, params)
        self.element_init()
        self.game_mode = params[0]
        pygame.mixer.stop()
        self.background_music = pygame.mixer.Sound(file = "assets/audio/level select.wav")
        self.background_music.play(loops=-1, fade_ms=2000)


    def element_init(self):
        """
        Initializes all UI elements
        """
        self.buttons = []
        self.background = PictureBox(0, 0, pygame.image.load("assets/background.jpg").convert())

        # static element init
        self.static_elements = []
        self.static_elements.append(TextBox(40, "select players"))
        self.static_elements[0].x = (self.width - self.static_elements[0].get_dimensions()[0]) / 2
        self.static_elements[0].y = self.height * 0.07
        self.static_elements.append(TextBox(40))
        self.static_elements[1].x = (self.width - self.static_elements[1].get_dimensions()[0]) / 2
        self.static_elements[1].y = self.height * 0.68
        self.static_elements.append(TextBox(20, "Back"))
        self.static_elements[2].x = self.width - self.static_elements[2].get_dimensions()[0] - 60
        self.static_elements[2].y = self.height - self.static_elements[2].get_dimensions()[1]*1.7
        self.static_elements.append(PictureBox(self.static_elements[2].x + self.static_elements[2].get_dimensions()[0] + 5, self.height - 53, \
                                    pygame.transform.scale(pygame.image.load("assets/icons/PS4_Circle.png").convert_alpha(), (45, 45))))
        self.static_elements.append(TextBox(20, "Select"))
        self.static_elements[4].x = self.static_elements[2].x - self.static_elements[4].get_dimensions()[0] - 60
        self.static_elements[4].y = self.height - self.static_elements[4].get_dimensions()[1]*1.7  
        self.static_elements.append(PictureBox(self.static_elements[4].x + self.static_elements[4].get_dimensions()[0] + 5, self.height - 53, \
                            pygame.transform.scale(pygame.image.load("assets/icons/PS4_Cross.png").convert_alpha(), (45, 45))))

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
        locked_players = []

        for selector in self.selectors:
            update_status = selector.update()
            if update_status[1] == True:
                locked_players.append(selector.player)
                selector.player.color = CharacterSelect.COLORS[selector.color_selection]
            elif selector.player == self.players[0] and update_status[0] == 0:
                not_joined = True

        if self.players[0] in locked_players and self.players[0].get_debounced_input(5):
            if self.game_mode == "main_game":
                return (1, "main_game", [locked_players, "levels/1.lvl"])
            elif self.game_mode == "legacy_game":
                if len(locked_players) >= 2:
                    return (1, "legacy_game", [locked_players])
                else:
                    self.static_elements[1].color = (0, 0, 0)
                    self.static_elements[1].background = True
                    self.static_elements[1].caption = "at least two players must be locked in"
                    self.static_elements[1].x = (self.width - self.static_elements[1].get_dimensions()[0]) / 2
        
        if self.players[0] not in locked_players or \
            self.players[0] in locked_players and len(locked_players) >=2:
            self.static_elements[1].background = False
            self.static_elements[1].caption = ""

        if self.players[0].get_debounced_input(6) and self.game_mode == "main_game":
            self.saver.find_save()

        if not_joined and self.players[0].get_debounced_input(7):
            return (1, "main_menu", [])

        return True

    def draw(self, screen, clock=None):
        screen.fill((255, 255, 255))
        self.background.draw(screen)
        for button in self.buttons:
            button.draw(screen)
        for element in self.static_elements:
            element.draw(screen)
        for selector in self.selectors:
            selector.draw(screen)

interfaces.interface_types["level_select"] = Level_Select