import pygame, time
from entity import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

class Projectile(Entity):

    def __init__(self, ID, health, width, height, x, y, x_speed, y_speed, damage, color):
        super().__init__(ID, health, width, height, x, y, width, damage, color)
        self._x_speed = x_speed
        self._y_speed = y_speed

    def _move(self, screen):
        self._x += self._x_speed
        self._y += self._y_speed
        pygame.draw.rect(screen, self._color, [self._x, self._y, self._width, self._height], 2)

    def collide(self, target):
        if target.get_ID() == self._ID:
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
        print(self._health)
        return self._x + self._width > 0 and self._x < screen_size[0] and \
            self._y + self._height > 0 and self._y < screen_size[1] and \
            self._health > 0 and (int(self._x_speed) != 0 or int(self._y_speed) != 0)

    def update(self, screen):
        self._move(screen)

class Player(Entity):
    def __init__(self, joystick, ID, health, width, height, x, y, hitbox, damage, color):
        super().__init__(ID, health, width, height, x, y, hitbox, damage, color)
        self._sensitivity = 3 # i think these two will always be true
        self._slowdown = 1
        self._threshold = 0.08
        self._joystick = joystick # grabs this players joystick object
        joystick.init() # initializes joysticks
        self._map = [0, 1, 2, 3, 11] # maps joystick buttons, this mapping works with ps4 controllers
    
    def get_init(self):
        status = self._joystick.get_init()

        if status == 0:
            self._joystick.quit()

        return status

    def _draw(self, screen):
        screen_size = screen.get_size()

        pygame.draw.rect(screen, self._color, \
            [self._x, self._y, self._width, self._height], 2)
        pygame.draw.rect(screen, self._color, \
            [self._x + (self._width - self._hitbox_size)/2, \
            self._y + (self._height - self._hitbox_size)/2, \
            self._hitbox_size, self._hitbox_size], 2)

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
            projs.append(Projectile(self._ID, self._damage, 4, 4, self._x + self._width / 2 - 2, \
                    self._y + self._height/2 - 2, self._sensitivity*joy_input[2], \
                    self._sensitivity*joy_input[3], self._damage, self._color))

    def _get_input(self):
        return [self._joystick.get_axis(self._map[0]), \
                self._joystick.get_axis(self._map[1]), \
                self._joystick.get_axis(self._map[2]), \
                self._joystick.get_axis(self._map[3]), \
                self._joystick.get_button(self._map[4])]

    def update(self, projs, screen):
        screen_size = screen.get_size()
        self._move(screen)
        self._shoot(projs)

class Boss(Entity):
    def __init__(self, ID, health, width, height, x, y, x_speed, y_speed, damage, color):
        super().__init__(ID, health, width, height, x, y, width, damage, color)
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
        if time.time() - self._moves[0][0] > self._moves[0][1]:
            self._moves[0] = (.5, time.time())
            i = 0
            x = -1.0
            y = -1.0
            while(i < 20):
                projs.append(Projectile(self._ID, self._damage, 5, 5, self._x + self._width / 2, self._y + self._height / 2, x*3, y*3, 10, BLACK))
                projs.append(Projectile(self._ID, self._damage, 5, 5, self._x + self._width / 2, self._y + self._height / 2, x*-3, y*3, 10, BLACK))
                x += 0.1
                y += 0.1
                i += 1
        if time.time() - self._moves[1][0] > self._moves[1][1]:
            self._moves[1] = (2.5, time.time())
            i = 0
            x = -1.0
            y =  0.0
            while(i < 20):
                projs.append(Projectile(self._ID, self._damage, 5, 5, self._x + self._width / 2, self._y + self._height / 2, x*3, y*3, 10, BLACK))
                projs.append(Projectile(self._ID, self._damage, 5, 5, self._x + self._width / 2, self._y + self._height / 2, x*-3, y*3, 10, BLACK))
                x += 0.1
                y += 0.1
                i += 1

        if time.time() - self._moves[2][0] > self._moves[2][1]:
            self._moves[2] = (0.2, time.time())
            i = 0
            x = -1.0
            y =  0.0
            while(i < 20):
                projs.append(Projectile(self._ID, self._damage, 5, 5, self._x + self._width / 2, self._y + self._height / 2, x*3, y*3, 10, BLACK))
                projs.append(Projectile(self._ID, self._damage, 5, 5, self._x + self._width / 2, self._y + self._height / 2, x*-3, y*3, 10, BLACK))
                x += 0.1
                y += 0.1
                i += 1


    def update_health(self, damage):
        self._health += damage

    def get_health(self):
        return self._health

    def get_ID(self):
        return self._ID

    def get_coords(self):
        return (self._x + (self._width - self._hitbox_size)/2, \
            self._y + (self._height - self._hitbox_size)/2, \
            self._hitbox_size, self._hitbox_size)

    def update(self, projs, screen):
        self._move(screen)
        self._attack(projs)