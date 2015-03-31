import pygame
from math import copysign
from entities.entity import Entity
import entities
from entities.projectiles import *
from entities.patterns import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

class Player(Entity):
    def __init__(self, ID, joystick, damage=5, color=RED):
        super().__init__(ID, damage, color)
        self._hitbox = 5
        self._sensitivity = 25 # in px/s
        self._shoot_sensitivity = 20
        self._slowdown = 10
        self._threshold = 0.08
        self._joystick = joystick # grabs this players joystick object
        self._map = [] # key bindings
        joystick.init() # initializes joysticks
        self._check_init() # makes sure joystick initialized succesfully
    
    def _check_init(self):
        if self._joystick.get_init():
            self._map_joystick() # joystick is good lets map it
        else:
            self._joystick.quit()

    def _map_joystick(self):
        if self._joystick.get_name() == "Wireless Controller":
            self._map = [0, 1, 2, 3, 4] # PS4 controller
        elif self._joystick.get_name() == "PLAYSTATION(R)3 Controller":
            self._map = [0, 1, 2, 3, 11] # PS3 controller
        else:
            self._map = [0, 1, 2, 3, 11] # default

    def _move(self, screen, dt):
        joy_input = self._get_input()
        screen_size = screen.get_size()

        if abs(joy_input[0]) > self._threshold:
            self._x += (self._sensitivity - (self._slowdown*joy_input[4]))*joy_input[0] * 20 * dt
            if self._x < 0:
                self._x = 0
            elif self._x + self._width > screen_size[0]:
                self._x = screen_size[0] - self._width

        if abs(joy_input[1]) > self._threshold:
            self._y += (self._sensitivity - (self._slowdown*joy_input[4]))*joy_input[1] * 20 * dt
            if self._y < 0:
                self._y = 0
            elif self._y + self._height > screen_size[1]:
                self._y = screen_size[1] - self._height

        self.center = self.get_center()
        #self._draw(screen)


    def _shoot(self, projs):
        joy_input = self._get_input()
        center = self.get_center()

        if abs(joy_input[2]) > self._threshold or abs(joy_input[3]) > self._threshold:
            proj = StraightProjectile(self._ID, center[0], center[1], \
                (5, 5, 5, self._shoot_sensitivity*joy_input[2] * 100, self._shoot_sensitivity*joy_input[3] * 100))
            proj.color = self._color
            projs.append(proj)
            proj.in_list = projs

    def _get_input(self):
        return [self._joystick.get_axis(self._map[0]), \
                self._joystick.get_axis(self._map[1]), \
                self._joystick.get_axis(self._map[2]), \
                self._joystick.get_axis(self._map[3]), \
                self._joystick.get_button(self._map[4])]

    def get_init(self):
        return self._joystick.get_init()

    def update(self, projs, screen, dt):
        screen_size = screen.get_size()
        self._move(screen, dt)
        self._shoot(projs)

    def despawn(self):
        # players will do something else eventually
        super().despawn()

class Enemy(Entity):
    def __init__(self, ID, pattern, proj):
        super().__init__(ID)
        # these need to be passed by the loader
        self._pattern = pattern
        self._pattern_params = None
        self._projectile = proj
        self._projectile_params = None
        self._direction = 0

        self._x_speed = None
        self._x_init = None
        self._y_speed = None

    # an enemy's x, y, x_speed, y_speed must be set before moving it
    # so that pattern knows what to do
    def _move(self, screen, dt):
        self._x_speed, self._y_speed = self._pattern(self, screen, dt, self._pattern_params)
        self._direction = 0 if self._x_speed == 0 else copysign(1, float(self._x_speed))
        self._x += self._x_speed * dt
        self._y += self._y_speed * dt
        self.center = self.get_center()

    def _attack(self, projs):
        if self.wait_to_shoot:
            if self._x_speed != 0 or self._y_speed != 0:
                return
        shot_time = pygame.time.get_ticks()
        # self.shot_time should be set in the loader
        if shot_time - self.shot_time >= 1000/self.fire_rate:
            if self._projectile == FallingProjectile:
                proj = self._projectile(self._ID, self.center[0], self.center[1], self._direction, self._projectile_params)
            else:
                proj = self._projectile(self._ID, self.center[0], self.center[1], self._projectile_params)
            projs.append(proj)
            proj.in_list = projs
            self.shot_time = shot_time

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        self._pattern = pattern

    @property
    def pattern_params(self):
        return self._pattern_params

    @pattern_params.setter
    def pattern_params(self, params):
        self._pattern_params = params
    
    @property
    def projectile_params(self):
        return self._projectile_params

    @projectile_params.setter
    def projectile_params(self, params):
        self._projectile_params = params
    
    @property
    def projectile(self):
        return self._projectile
    @projectile.setter
    def projectile(self, proj):
        self._projectile = proj

    @property
    def x_speed(self):
        return self._x_speed

    @x_speed.setter
    def x_speed(self, x_speed):
        self._x_speed = x_speed

    @property
    def x_init(self):
        return self._x_init
    @x_init.setter

    def x_init(self, value):
        self._x_init = value

    @property
    def y_speed(self):
        return self._y_speed

    @y_speed.setter
    def y_speed(self, y_speed):
        self._y_speed = y_speed

    def update(self, projs, screen, dt):
        super().update()
        self._move(screen, dt)
        self._attack(projs)

# class Boss(Entity):
#     def __init__(self, ID, pattern, proj):
#         super().__init__(ID)
#         # these need to be passed by the loader
#         self._pattern = pattern
#         self._pattern_params = None
#         self._projectile = proj
#         self._projectile_params = None

#         self._x_speed = None # in px/s
#         self._y_speed = None

#     def _move(self, screen, dt):
#         screen_size = screen.get_size()
#         self._x_speed, self._y_speed = self._pattern(self, screen, 200)
#         self._x += self._x_speed * dt
#         self._y += self._y_speed * dt

#     def _attack(self, projs):
#         # proj = StraightProjectile(self._ID, self._x, self._y, 0, 200)
#         proj = (self._ID, self._x + self._width/2, self._y + self._height/2, 50, 100, sign(self._x_speed))
#         proj.health = 5
#         proj.width = 5
#         proj.height = 5
#         projs.append(proj)

#     def update(self, projs, screen, dt):
#         self._move(screen, dt)
#         self._attack(projs)

entities.entity_types["Enemy"] = Enemy
# entities.entity_types["Boss"] = Boss