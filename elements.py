"""
Contains some UI elements classes such as, buttons, textboxess etc
"""
import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)

class Button:
    def __init__(self, x, y, width, height, event, caption=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.event = event
        self.selected = 0
        self.color = (BLACK, RED)
        self.font_size = 40
        self.font = pygame.font.SysFont("Roboto", self.font_size)
        self.caption = caption

    def draw(self, screen):
        pygame.draw.rect(screen, self.color[self.selected], (self.x, self.y, self.width, self.height), 2)
        textBitmap = self.font.render(self.caption, True, (0, 0, 0))
        x = (self.width - textBitmap.get_size()[0]) / 2 + self.x
        y = (self.height - textBitmap.get_size()[1]) / 2 + self.y
        screen.blit(textBitmap, [x, y])

class TextBox:
    def __init__(self, font, font_size, caption=""):
        self.color = BLACK
        self.font = pygame.font.SysFont(font, font_size)
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
