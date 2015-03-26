import pygame
from math import sqrt
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

    def _move(self, screen, dt):
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
            self._health > 0 and (int(self._x_speed) != 0 or int(self._y_speed) != 0)

    def update(self, screen, dt):
        self._move(screen, dt)

class StraightProjectile(Projectile):
    def __init__(self, ID, x, y, x_speed, y_speed):
        super().__init__(ID, x, y)
        self._x_speed = x_speed # in px/s
        self._y_speed = y_speed

    def _move(self, screen, dt):
        self._x += self._x_speed * dt
        self._y += self._y_speed * dt
        #pygame.draw.rect(screen, self._color, [self._x, self._y, self._width, self._height], 2)

class FallingProjectile(Projectile):
    def __init__(self, ID, x, y, x_speed, gravity, direction):
        # x_move: px/s  gravity: px/s^2
        super().__init__(ID, x, y)
        self._x_speed = x_speed # in px/s
        self._y_speed = 0
        self._gravity = gravity
        self._direction = direction # 1 or -1

    def _move(self, screen, dt):
        self._x += self._x_speed * dt * self._direction
        self._y += self._y_speed * dt + self._gravity * dt * dt / 2
        self._y_speed += self._gravity * dt
        #pygame.draw.rect(screen, self._color, [self._x, self._y, self._width, self._height], 2)

class TargetedProjectile(Projectile):
    def __init__(self, ID, x, y, speed, target):
        super().__init__(ID, x, y)
        self._target = target
        self._speed = speed

        if target is None:
            self._x_speed = 0
            self._y_speed = 0
        else:
            # direction math
            x_diff = target.x - self._x
            y_diff = target.y - self._y
            hyp = sqrt(x_diff**2 + y_diff**2)
            self._x_speed = self._speed * x_diff / hyp
            self._y_speed = self._speed * y_diff / hyp

    def _move(self, screen, dt):
        self._x += self._x_speed * dt
        self._y += self._y_speed * dt


