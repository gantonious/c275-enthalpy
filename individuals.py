import pygame, time
from entity import *
from projectiles import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

class Player(Entity):
    def __init__(self, ID, joystick, damage=5, color=RED):
        super().__init__(ID, damage, color)
        self._hitbox = 5
        self._sensitivity = 3 # i think these two will always be true
        self._shoot_sensitivity = 20
        self._slowdown = 1
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

    def _draw(self, screen):
        screen_size = screen.get_size()

        pygame.draw.rect(screen, self._color, \
            [self._x, self._y, self._width, self._height], 2)
        pygame.draw.rect(screen, self._color, \
            [self._x + (self._width - self._hitbox)/2, \
            self._y + (self._height - self._hitbox)/2, \
            self._hitbox, self._hitbox], 2)

    def _move(self, screen):
        joy_input = self._get_input()
        screen_size = screen.get_size()

        # number crunching, these magic numbers are the screen dimensions ill get rid of them soon

        if abs(joy_input[0]) > self._threshold:
            self._x += (self._sensitivity - (self._slowdown*joy_input[4]))*joy_input[0]
            if self._x < 0:
                self._x = 0
            elif self._x + self._width > screen_size[0]:
                self._x = screen_size[0] - self._width

        if abs(joy_input[1]) > self._threshold:
            self._y += (self._sensitivity - (self._slowdown*joy_input[4]))*joy_input[1]
            if self._y < 0:
                self._y = 0
            elif self._y + self._height > screen_size[1]:
                self._y = screen_size[1] - self._height

        self._draw(screen)


    def _shoot(self, projs):
        joy_input = self._get_input()

        if abs(joy_input[2]) > self._threshold or abs(joy_input[3]) > self._threshold:
            # projs.append(StraightProjectile(self._ID, self._damage, 4, 4, self._x + self._width / 2 - 2, \
            #         self._y + self._height/2 - 2, self._shoot_sensitivity*joy_input[2], \
            #         self._shoot_sensitivity*joy_input[3], self._damage, self._color))
            proj = StraightProjectile(self._ID, self._x, self._y, \
                self._shoot_sensitivity*joy_input[2], self._shoot_sensitivity*joy_input[3])
            proj.health = 5
            proj.width = 5
            proj.height = 5
            proj.color = self._color
            projs.append(proj)

    def _get_input(self):
        return [self._joystick.get_axis(self._map[0]), \
                self._joystick.get_axis(self._map[1]), \
                self._joystick.get_axis(self._map[2]), \
                self._joystick.get_axis(self._map[3]), \
                self._joystick.get_button(self._map[4])]

    def get_init(self):
        return self._joystick.get_init()

    def update(self, projs, screen):
        screen_size = screen.get_size()
        self._move(screen)
        self._shoot(projs)

# class Enemy(Entity):
#     def __init__(self, ID):
#         super().__init__(ID)

#     def _move(self, screen):
#         screen_size = screen.get_size()
#         # do some movement stuff

class Boss(Entity):
    def __init__(self, ID, x_speed, y_speed):
        super().__init__(ID)
        self._x_speed = x_speed
        self._y_speed = y_speed
        self._moves = [(0, 0), (2, 0), (0, 0)] # tuples containg move and countdown

    def _move(self, screen):
        screen_size = screen.get_size()
        if self._x < 0:
            self._x_speed = 30
        elif self._x > screen_size[0]:
            self._x_speed = -30
        self._x += self._x_speed
        self._y += self._y_speed
        pygame.draw.rect(screen, self._color, [self._x, self._y, self._width, self._height], 2)

    def _attack(self, projs):
        """
        """
        proj = StraightProjectile(self._ID, self._x, self._y, 0, 5)
        # proj = FallingProjectile(self._ID, self._x, self._y, 2, 1.01)
        proj.health = 5
        proj.width = 5
        proj.height = 5
        projs.append(proj)

    def update(self, projs, screen):
        self._move(screen)
        self._attack(projs)