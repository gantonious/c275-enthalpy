import pygame
from entity import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

class Projectile(Entity):

    def __init__(self, ID, x, y):
        # stuff that needs to be set: health, size
        super().__init__(ID)
        self._x = x
        self._y = y

    def _move(self, screen):
        # python pls don't be mad
        pass

    def collide(self, target):
        if target.ID == self._ID:
            return 0
        coords = target.get_coords()
        if (self._x + self._width > coords[0] and \
            self._x < coords[0] + coords[2] and \
            self._y + self._height > coords[1] and \
            self._y < coords[1] + coords[3]):
            self._health -= target._damage
            target.update_health(-1*self._damage)
            return 1
        return 0

    def on_screen(self, screen):
        screen_size = screen.get_size()
        return self._x + self._width > 0 and self._x < screen_size[0] and \
            self._y + self._height > 0 and self._y < screen_size[1] and \
            self._health > 0 and (int(self._x_move) != 0 or int(self._y_move) != 0)

    def update(self, screen):
        self._move(screen)

class StraightProjectile(Projectile):
    def __init__(self, ID, x, y, x_move, y_move):
        super().__init__(ID, x, y)
        self._x_move = x_move
        self._y_move = y_move

    def _move(self, screen):
        self._x += self._x_move
        self._y += self._y_move
        pygame.draw.rect(screen, self._color, [self._x, self._y, self._width, self._height], 2)

class FallingProjectile(Projectile):
    def __init__(self, ID, x, y, x_move, gravity):
        super().__init__(ID, x, y)
        self._x_move = x_move
        self._original_y = y
        self._gravity = gravity

    def _move(self, screen, dt):
        pass








