import pygame
from math import sqrt, sin, cos, pi
from entities.entity import Entity
import entities

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

class Projectile(Entity):

    def __init__(self, ID, shooter, x, y):
        # stuff that needs to be set: health, size
        super().__init__(ID)
        self._x = x
        self._y = y
        self._hitbox = self._x
        self.shooter = shooter

    def _move(self, dimensions, dt):
        # python pls don't be mad
        pass

    def update(self, dimensions, dt):
        self._move(dimensions, dt)
        super().update(dimensions)
        if not self.on_screen(dimensions):
            self.despawn()

class StraightProjectile(Projectile):

    targets = False

    def __init__(self, ID, shooter, x, y, params):
        # to be passed: health, width, height, x_speed, y_speed
        super().__init__(ID, shooter, x, y)
        self._health = int(params[0])
        self._width = int(params[1])
        self._height = int(params[2])
        self._x_speed = int(params[3]) # in px/s
        self._y_speed = int(params[4])

    def _move(self, dimensions, dt):
        self._x += self._x_speed * dt
        self._y += self._y_speed * dt

class SunburstProjectiles(Projectile):

    targets = False

    def __init__(self, ID, shooter, x, y, params):
        super().__init__(ID, shooter, x, y)
        self._projectile_params = [int(params[0]), int(params[1]), int(params[2])]
        self._health = 0
        self._width = 0
        self._height = 0
        self._speed = int(params[3])
        self._shots = int(params[4])
        self._turn = int(params[5])
        try:
            self.shooter.turn
        except AttributeError:
            self.shooter.turn = 0 # shots per turn

    # this method creates the actual sunburst, then the sunburst object despawns
    def update(self, dimensions, dt):
        for i in range(self._shots):
            if i == 0:
                x_speed = self._speed*cos(self.shooter.turn*2*pi/self._turn)
                y_speed = self._speed*sin(self.shooter.turn*2*pi/self._turn)
            else:
                x_speed = self._speed*cos(2*pi/self._shots*i + self.shooter.turn*2*pi/self._turn)
                y_speed = self._speed*sin(2*pi/self._shots*i + self.shooter.turn*2*pi/self._turn)
            proj = StraightProjectile(self._ID, self.shooter, self._x, self._y, self._projectile_params + [x_speed, y_speed])
            self.in_list.append(proj)
            proj.in_list = self.in_list
        self.shooter.turn += 1
        self.despawn()

class FallingProjectile(Projectile):

    targets = False

    def __init__(self, ID, shooter, x, y, direction, params):
        # to be passed: health, width, height, speed, gravity
        # gravity: px/s^2
        super().__init__(ID, shooter, x, y)
        self._health = int(params[0])
        self._width = int(params[1])
        self._height = int(params[2])
        self._x_speed = int(params[3]) # in px/s
        self._gravity = int(params[4])
        self._direction = direction
        self._y_speed = 0

    def _move(self, dimensions, dt):
        self._x += self._x_speed * dt * self._direction
        self._y += self._y_speed * dt + self._gravity * dt * dt / 2
        self._y_speed += self._gravity * dt

class TargetedProjectile(Projectile):

    targets = True

    def __init__(self, ID, shooter, x, y, params):
        super().__init__(ID, shooter, x, y)
        # to be passed: health, width, height, speed, target
        self._health = int(params[0])
        self._width = int(params[1])
        self._height = int(params[2])
        self._speed = int(params[3])
        self.target = params[4]

        if self.target is None:
            self._x_speed = 0
            self._y_speed = 0
        else:
            # direction math
            self_center = self.get_center()
            target_center = self.target.get_center()
            x_diff = target_center[0] - self_center[0]
            y_diff = target_center[1] - self_center[1]
            hyp = sqrt(x_diff**2 + y_diff**2)
            self._x_speed = self._speed * x_diff / hyp
            self._y_speed = self._speed * y_diff / hyp

    def _move(self, dimensions, dt):
        if self.target is None:
            self.despawn() # i have to do this here so that despawn() doesn't get mad
        self._x += self._x_speed * dt
        self._y += self._y_speed * dt

class DoNothing(Projectile):

    targets = False

    def __init__(self, ID, shooter, x, y, params):
        super().__init__(ID, shooter, x, y)
        self._width = 0
        self._height = 0

    def update(self, screen, dt):
        self.despawn()

entities.entity_types["Straight"] = StraightProjectile
entities.entity_types["Sunburst"] = SunburstProjectiles
entities.entity_types["Falling"] = FallingProjectile
entities.entity_types["Targeted"] = TargetedProjectile
entities.entity_types["DoNothing"] = DoNothing