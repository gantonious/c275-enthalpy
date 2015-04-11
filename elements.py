"""
Contains some UI element classes such as, buttons, textboxes etc
"""
import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)
ORANGE   = ( 255, 127,  39)

class Button:
    """
    Button class that can be selected and has an event associated with it
    """
    def __init__(self, x, y, width, height, event, caption=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.event = event
        self.selected = 0
        self.color = (BLACK, WHITE)
        self.alpha = (100, 150)
        self.font_size = int(self.height / 2.5)
        self.caption = caption

    def draw(self, screen):
        self.font = pygame.font.Font("assets/Roboto-Thin.ttf", self.font_size)
        button_background = pygame.Surface((self.width, self.height))
        button_background.set_alpha(self.alpha[self.selected])
        button_background.fill(WHITE)
        screen.blit(button_background, [self.x, self.y])
        pygame.draw.rect(screen, self.color[self.selected], (self.x, self.y, self.width, self.height), 2)
        textBitmap = self.font.render(self.caption, True, (0, 0, 0))
        x = (self.width - textBitmap.get_size()[0]) / 2 + self.x
        y = (self.height - textBitmap.get_size()[1]) / 2 + self.y
        screen.blit(textBitmap, [x, y])

class RadioButtons:
    """
    A class that handles having multiple buttons arranged vertically
    where only one button can be selected at a time
    """
    def __init__(self, x, y, button_width, button_height, orientation, players):
        self.buttons = []
        self.players = players
        self.threshold = 0.08
        self.y_spacing = button_height * 0.25
        self.x_spacing = button_width * 0.25
        self.x = x
        self.y = y
        self.button_width = button_width
        self.button_height = button_height
        self._select_colors = (BLACK, WHITE)
        self.orientation = orientation # 0 for vert 1 for hor
        self.selected_button = None
        self.stick_debounce = [0, 250]
        self.stick_map = [(1, 3), (0, 2)]

    @property
    def select_colors(self):
        return self._select_colors
    
    @select_colors.setter
    def select_colors(self, select_colors):
        for button in self.buttons:
            button.color = select_colors
        self._select_colors = select_colors

    def add_radio_button(self, event, caption):
        if self.orientation == 0:
            self.buttons.append(Button(self.x, self.y + len(self.buttons) * (self.y_spacing + self.button_height), \
                            self.button_width, self.button_height, event, caption))
        elif self.orientation == 1:
            self.buttons.append(Button(self.x + len(self.buttons) * (self.x_spacing + self.button_width), self.y, \
                                        self.button_width, self.button_height, event, caption))
        self.buttons[-1].color = self._select_colors

    def select_button(self, target_button):
        for button in self.buttons:
            button.selected = 0
        target_button.selected = 1
        self.selected_button = target_button
        self.stick_debounce[0] = pygame.time.get_ticks()

    def update(self):
        if self.selected_button == None:
            self.select_button(self.buttons[0])

        if self.players:
            if pygame.time.get_ticks() - self.stick_debounce[0] > self.stick_debounce[1]:
                for button in enumerate(self.buttons):
                    if button[0] == 0:
                        # check the second button is selected and player is moving up/left in the menu
                        if (self.players[0].get_input()[self.stick_map[self.orientation][0]] < -self.threshold \
                            or self.players[0].get_input()[self.stick_map[self.orientation][1]] < -self.threshold) and self.buttons[button[0] + 1].selected == 1:
                            self.select_button(button[1])
                            break  
                    elif button[0] == (len(self.buttons) - 1):
                        # check if the second last button is selected and the player is moving down/right in menu 
                        if (self.players[0].get_input()[self.stick_map[self.orientation][0]] > self.threshold or \
                            self.players[0].get_input()[self.stick_map[self.orientation][1]] > self.threshold) and self.buttons[button[0] - 1].selected == 1:
                            self.select_button(button[1])
                            break  
                    else:
                        # check if any button that is not the first of last is selected and player is moving 
                        # up/left from the next button or down/right from the previous
                        if ((self.players[0].get_input()[self.stick_map[self.orientation][0]] > self.threshold or \
                            self.players[0].get_input()[self.stick_map[self.orientation][1]] > self.threshold) and self.buttons[button[0] - 1].selected == 1) \
                            or ((self.players[0].get_input()[self.stick_map[self.orientation][0]] < -self.threshold or \
                            self.players[0].get_input()[self.stick_map[self.orientation][1]] < -self.threshold) and self.buttons[button[0] + 1].selected == 1):
                            self.select_button(button[1])
                            break

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

class TextBox:
    """
    Simple box of text that can have different colors and fonts etc
    """
    def __init__(self, font_size, caption=""):
        self._color = BLACK
        self._font_face = "Roboto-Thin.ttf"
        self.font_size = font_size
        self.caption = caption
        self.background = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
    
    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        # render text again when we update it
        self._caption = caption
        self.render_text()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size
        self.font = pygame.font.Font("assets/" + self.font_face, self.font_size)

    @property
    def font_face(self):
        return self._font_face

    @font_face.setter
    def font_face(self, font_face):
        try:
            self.font = pygame.font.Font("assets/" + font_face, self.font_size)
            self._font_face = font_face
        except:
            pass

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color
        self.render_text()

    def render_text(self):
        self.textBitmap = self.font.render(self.caption, True, self.color)

    def get_dimensions(self):
        return self.textBitmap.get_size()

    def draw(self, screen):
        if self.background:
            text_background = pygame.Surface((self.get_dimensions()[0] + self.font_size / 2, self.get_dimensions()[1] + self.font_size / 2))
            text_background.set_alpha(150)
            text_background.fill(WHITE)
            screen.blit(text_background, [self.x - self.font_size / 4, self.y - self.font_size / 4])
            pygame.draw.rect(screen, BLACK, (self.x - self.font_size / 4, self.y - self.font_size / 4, self.get_dimensions()[0] + self.font_size / 2, self.get_dimensions()[1] + self.font_size / 2), 2)
        screen.blit(self.textBitmap, [self._x, self._y])

class PictureBox:
    """
    Simple picture box with specified coordinates and an image
    """
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self._image = image

    def get_dimensions(self):
        return self._image.get_size()

    def draw(self, screen):
        screen.blit(self._image, [self.x, self.y])

class CharacterStatusBar:
    """
    Used to draw the status information of a character to the screen
    in a status box 
    """
    def __init__(self, x, y, width, height, player):
        self.x = x
        self.y = y
        self.width = width
        self.height = height  
        self.player = player

    def draw(self, screen):
        background = pygame.Surface((self.width, self.height))
        background.set_alpha(150)
        background.fill(WHITE)
        screen.blit(background, [self.x, self.y])
        pygame.draw.rect(screen, self.player.color, (self.x, self.y, self.width, self.height), 2)

        health_bar_x = self.width * 0.4 + self.x
        health_bar_y = self.height * 0.22 + self.y
        health_bar_width = self.width * 0.55
        health_bar_height = self.height * 0.15

        pygame.draw.rect(screen, self.player.color, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 1)
        pygame.draw.rect(screen, self.player.color, (health_bar_x, health_bar_y, max(0, self.player.health * health_bar_width / self.player.max_health), health_bar_height))

        font_size = int(self.height * 0.62)
        font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
        textBitmap = font.render("P" + str(self.player.ID + 1), True, self.player.color) 
        screen.blit(textBitmap, \
                    [self.x + self.width * 0.1, \
                    (self.height - textBitmap.get_size()[1]) / 2 + self.y])

        font_size = int(self.height * 0.4)
        font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
        textBitmap = font.render(str(self.player.score), True, self.player.color) 
        screen.blit(textBitmap, \
                [self.width * 0.95 + self.x - textBitmap.get_size()[0], \
                self.y + self.height * 0.50])


class CharacterSelect:
    """
    Used to select a color and lock in a player for gameplay
    """
    COLORS = [RED, GREEN, ORANGE, BLUE]
    def __init__(self, x, y, width, height, player):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.target_height = self.height
        self.player = player
        self.state = 0
        self.color_selection = 0
        self.stick_debounce = [0, 250]
        self.threshold = 0.08
        self.animating = False

    def update(self):
        self.vertical_slide()

        if not self.animating:
            if self.state == 0 and self.player.get_debounced_input(5):
                # player joins game
                self.state = 1
            elif self.state == 1:
                if pygame.time.get_ticks() - self.stick_debounce[0] > self.stick_debounce[1]:
                    # player selects from the available colors
                    if self.player.get_input()[0] < -self.threshold or self.player.get_input()[2] < -self.threshold:
                        self.color_selection = (self.color_selection - 1) % len(CharacterSelect.COLORS)
                        self.stick_debounce[0] = pygame.time.get_ticks()
                    elif self.player.get_input()[0] > self.threshold or self.player.get_input()[2] > self.threshold:
                        self.color_selection = (self.color_selection + 1) % len(CharacterSelect.COLORS)
                        self.stick_debounce[0] = pygame.time.get_ticks()
                if self.player.get_debounced_input(5):
                    # player is locked in
                    self.target_height = self.height * 0.5
                    self.state = 2
                elif self.player.get_debounced_input(7):
                    # player backs out of game
                    self.state = 0
            elif self.state == 2:
                if self.player.get_debounced_input(7):
                    # player is not locked in
                    self.target_height = self.height * 2
                    self.state = 1

        return self.state

    def vertical_slide(self):
        move_factor = 10
        if abs(self.height - self.target_height) < move_factor:
            self.height = self.target_height
            self.animating = False
        elif self.height - self.target_height > 0:
            self.height -= move_factor
            self.animating = True
        elif self.height - self.target_height < 0:
            self.height += move_factor 
            self.animating = True

    def draw(self, screen):
        background = pygame.Surface((self.width, self.height))
        background.set_alpha(150)
        background.fill(WHITE)
        screen.blit(background, [self.x, self.y])

        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        font_size = 30
        font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
        textBitmap = font.render("player " + str(self.player.ID + 1), True, (0, 0, 0)) 
        screen.blit(textBitmap, \
                    [(self.width - textBitmap.get_size()[0]) / 2 + self.x, \
                      textBitmap.get_size()[1] * 0.6 + self.y])
        if self.state == 0:
            font_size = 20
            font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
            textBitmap = font.render("press x to join", True, (0, 0, 0)) 
            screen.blit(textBitmap, \
                        [(self.width - textBitmap.get_size()[0]) / 2  + self.x, \
                          self.height * 0.5 + self.y])
        elif self.state == 1:
            pygame.draw.rect(screen, CharacterSelect.COLORS[self.color_selection], 
                            (self.width*0.35 + self.x, self.height*0.4 + self.y, \
                             self.width*0.3, self.width*0.3), 2)
            font_size = 20
            font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
            textBitmap = font.render("<< select a color >>", True, (0, 0, 0)) 
            screen.blit(textBitmap, \
                        [(self.width - textBitmap.get_size()[0]) / 2 + self.x, \
                        self.height * 0.8 + self.y])
        elif self.state == 2:
            font_size = 18
            font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
            textBitmap = font.render("ready, press o to unready", True, (0, 0, 0)) 
            screen.blit(textBitmap, \
                        [(self.width - textBitmap.get_size()[0]) / 2 + self.x, \
                        self.height * 0.68 + self.y])

class CharacterClearStatus:
    """
    Provides information about the player while progressing through the levels,
    is also used to lock in players for further rounds of gameplay
    """
    def __init__(self, x, y, width, height, player, ready_functionality):
        self.x = x
        self.y = y
        self.width = width
        self.target_width = width
        self.height = height
        self.player = player
        self.state = False
        self.animating = False
        self.ready_functionality = ready_functionality

    def update(self):
        self.horizontal_slide()

        if not self.animating and self.ready_functionality:
            if not self.state and self.player.get_debounced_input(5):
                # player locked in
                self.state = True
                self.target_width = self.width * 0.90
            elif self.state and self.player.get_debounced_input(7):
                # player not locked in
                self.state = False
                self.target_width = self.width * 10 / 9

        return self.state

    def horizontal_slide(self):
        move_factor = 10
        if abs(self.width - self.target_width) < move_factor:
            self.width = self.target_width
            self.animating = False
        elif self.width - self.target_width > 0:
            self.width -= move_factor
            self.animating = True
        elif self.width - self.target_width < 0:
            self.width += move_factor 
            self.animating = True

    def draw(self, screen):
        background = pygame.Surface((self.width, self.height))
        background.set_alpha(150)
        background.fill(WHITE)
        screen.blit(background, [self.x, self.y])
        pygame.draw.rect(screen, self.player.color, (self.x, self.y, self.width, self.height), 2)

        font_size = int(self.height * 0.62)
        font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
        textBitmap = font.render("player " + str(self.player.ID + 1), True, (0, 0, 0)) 
        screen.blit(textBitmap, \
                    [self.x + 25, \
                    (self.height - textBitmap.get_size()[1]) / 2 + self.y])

        player_name_width = textBitmap.get_size()[0]

        font_size = int(self.height * 0.4)
        font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
        textBitmap = font.render("score: " + str(self.player.score) + "    enemies killed: " + str(self.player.kills[0]) + \
                                 "    bros killed: " + str(self.player.kills[1]), True, (0, 0, 0))
        screen.blit(textBitmap, \
                    [self.x + player_name_width + 65, \
                    (self.height - textBitmap.get_size()[1]) / 2  + self.y])

        if self.ready_functionality:
            font_size = int(self.height * 0.62)
            font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
            if self.state:
                textBitmap = font.render("READY", True, (0, 0, 0)) 
            else:
                textBitmap = font.render("NOT READY", True, (0, 0, 0))

            screen.blit(textBitmap, \
                [self.width * 0.98 + self.x - textBitmap.get_size()[0], \
                (self.height - textBitmap.get_size()[1]) / 2  + self.y])

