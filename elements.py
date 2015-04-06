"""
Contains some UI elements classes such as, buttons, status_bars etc
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
    pass

class PictureBox:
    pass