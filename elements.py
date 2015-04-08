"""
Contains some UI element classes such as, buttons, textboxess etc
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
    def __init__(self, x, y, width, height, event, caption=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.event = event
        self.selected = 0
        self.color = (BLACK, RED, WHITE)
        self.font_size = 40
        self.caption = caption

    def draw(self, screen):
        self.font = pygame.font.Font("assets/Roboto-Thin.ttf", self.font_size)
        pygame.draw.rect(screen, self.color[2], (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.color[self.selected], (self.x, self.y, self.width, self.height), 2)
        textBitmap = self.font.render(self.caption, True, (0, 0, 0))
        x = (self.width - textBitmap.get_size()[0]) / 2 + self.x
        y = (self.height - textBitmap.get_size()[1]) / 2 + self.y
        screen.blit(textBitmap, [x, y])

class TextBox:
    def __init__(self, font_size, caption=""):
        self.color = BLACK
        self.font_size = font_size
        self.caption = caption

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
        self.font = pygame.font.Font("assets/Roboto-Thin.ttf", self.font_size)

    def render_text(self):
        self.textBitmap = self.font.render(self.caption, True, (0, 0, 0))

    def get_dimensions(self):
        return self.textBitmap.get_size()

    def draw(self, screen):
        screen.blit(self.textBitmap, [self._x, self._y])

class PictureBox:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self._image = image

    def get_dimensions(self):
        return self._image.get_size()

    def draw(self, screen):
        screen.blit(self._image, [self.x, self.y])


class CharacterSelect:
    COLORS = [RED, GREEN, ORANGE, BLUE]
    def __init__(self, x, y, width, height, player, ID):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.target_height = self.height
        self.player = player
        self.ID = ID
        self.state = 0
        self.color_selection = 0
        self.stick_debounce = [0, 250]
        self.threshold = 0.08
        self.animating = False

    def update(self):
        self.vertical_slide()

        if not self.animating:
            if self.state == 0 and self.player.get_debounced_input(5):
                self.state = 1
            elif self.state == 1:
                if pygame.time.get_ticks() - self.stick_debounce[0] > self.stick_debounce[1]:
                    if self.player.get_input()[0] < -self.threshold or self.player.get_input()[2] < -self.threshold:
                        self.color_selection = (self.color_selection - 1) % len(CharacterSelect.COLORS)
                        self.stick_debounce[0] = pygame.time.get_ticks()
                    elif self.player.get_input()[0] > self.threshold or self.player.get_input()[2] > self.threshold:
                        self.color_selection = (self.color_selection + 1) % len(CharacterSelect.COLORS)
                        self.stick_debounce[0] = pygame.time.get_ticks()
                if self.player.get_debounced_input(5):
                    self.target_height = self.height * 0.5
                    self.state = 2
                elif self.player.get_debounced_input(7):
                    self.state = 0
            elif self.state == 2:
                if self.player.get_debounced_input(7):
                    self.target_height = self.height * 2
                    self.state = 1

        if self.state == 2:
            return (self.state, True)
        else:
            return (self.state, False)

        return (-1, False)

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
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        font_size = 30
        font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
        textBitmap = font.render("player " + str(self.ID), True, (0, 0, 0)) 
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
                          self.height * 0.7 + self.y])

class CharacterClearStatus:
    def __init__(self, x, y, width, height, player, ID):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.player = player
        self.ID = ID

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.player.color, (self.x, self.y, self.width, self.height), 2)
        font_size = 40
        font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
        textBitmap = font.render("player " + str(self.ID), True, (0, 0, 0)) 
        screen.blit(textBitmap, \
                    [self.width * 0.05 + self.x, \
                      (self.height - textBitmap.get_size()[1]) / 2 + self.y])
        font_size = 25
        font = pygame.font.Font("assets/Roboto-Thin.ttf", font_size)
        textBitmap = font.render("score: " + str(self.player.score), True, (0, 0, 0)) 
        screen.blit(textBitmap, \
                    [self.width * 0.93 + self.x - textBitmap.get_size()[0], \
                      (self.height - textBitmap.get_size()[1]) / 2  + self.y])


