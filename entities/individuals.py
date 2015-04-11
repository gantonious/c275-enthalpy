import pygame
from math import copysign, sqrt
from entities.entity import Entity
import entities
from entities.projectiles import *
from entities.patterns import *
from entities.drops import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

class Player(Entity):
    def __init__(self, ID, joystick, damage=5, color=RED):
        super().__init__(ID, damage, color)
        self.score = 0
        self.proj_size = 10
        self._hitbox = 5
        self._sensitivity = 25 # in px/s
        self._shoot_sensitivity = 20
        self._slowdown = 10
        self._threshold = 0.08
        self._joystick = joystick # grabs this players joystick object
        self._map = [] # key bindings
        self._init_status = False
        joystick.init() # initializes joysticks
        self._check_init() # makes sure joystick initialized succesfully
        self._button_debounce = [1 for i in range(len(self._map))]
        self.invuln_active = False
        self.shotsize_active = False
    
    def _check_init(self):
        if self._joystick.get_init():
            self._map_joystick() # joystick is good lets map it
        else:
            self._joystick.quit()

    def _map_joystick(self):
        if self._joystick.get_name() == "Wireless Controller":
            self._map = [0, 1, 2, 3, 4, 1, 9, 2] # PS4 controller
            self._init_status = True
        elif self._joystick.get_name() == "PLAYSTATION(R)3 Controller":
            self._map = [0, 1, 2, 3, 11, 14, 3, 13] # PS3 controller
            self._init_status = True
        else:
            self._init_status = False # not a compatible controller
            self._joystick.quit()

    def _move(self, dimensions, dt):
        joy_input = self.get_input()

        if abs(joy_input[0]) > self._threshold:
            self._x += (self._sensitivity - (self._slowdown*joy_input[4]))*joy_input[0] * 20 * dt
            if self._x < dimensions[0]:
                self._x = dimensions[0]
            elif self._x + self._width > dimensions[0] + dimensions[2]:
                self._x = dimensions[0] + dimensions[2] - self._width

        if abs(joy_input[1]) > self._threshold:
            self._y += (self._sensitivity - (self._slowdown*joy_input[4]))*joy_input[1] * 20 * dt
            if self._y < dimensions[1]:
                self._y = dimensions[1]
            elif self._y + self._height > dimensions[1] + dimensions[3]:
                self._y = dimensions[1] + dimensions[3] - self._height

        self.center = self.get_center()
        #self._draw(screen)

    def _shoot(self, projs):
        joy_input = self.get_input()
        center = self.get_center()

        if abs(joy_input[2]) > self._threshold or abs(joy_input[3]) > self._threshold:
            x_factor = self._shoot_sensitivity*joy_input[2]
            y_factor = self._shoot_sensitivity*joy_input[3]
            hyp = sqrt(x_factor**2 + y_factor**2)
            shot_time = pygame.time.get_ticks()
            proj = StraightProjectile(self._ID, self, center[0], center[1], \
                (5, self.proj_size, self.proj_size, x_factor*1000/hyp, y_factor*1000/hyp))
            proj.color = self._color
            projs.append(proj)
            proj.in_list = projs

    def get_input(self):
        """
        Returns a list of inputs for each joystick binding
        """
        return [self._joystick.get_axis(self._map[0]), \
                self._joystick.get_axis(self._map[1]), \
                self._joystick.get_axis(self._map[2]), \
                self._joystick.get_axis(self._map[3]), \
                self._joystick.get_button(self._map[4]), \
                self._joystick.get_button(self._map[5]), \
                self._joystick.get_button(self._map[6]), \
                self._joystick.get_button(self._map[7])]

    def get_debounced_input(self, index):
        """
        Returns the debounced input of the specified joystick binding
        """
        raw_input = self.get_input()[index]

        if self._button_debounce[index]:
            debounced_input = 0
        else:
            debounced_input = raw_input
        self._button_debounce[index] = raw_input

        return debounced_input

    def get_init(self):
        return self._init_status

    def update(self, projs, dimensions, dt):
        self._move(dimensions, dt)
        self._shoot(projs)

    def despawn(self):
        # players will do something else eventually
        super().despawn()

class Enemy(Entity):
    def __init__(self, ID, pattern, proj):
        super().__init__(ID)
        # these need to be passed by the loader
        self._pattern = pattern[0]
        self._pattern_params = None
        self._projectile = proj[0]
        self._projectile_params = None
        self._direction = 0

        self._x_speed = None
        self._y_speed = None

    # an enemy's x, y, x_speed, y_speed must be set before moving it
    # so that pattern knows what to do
    def _move(self, dimensions, drop_list, dt):
        self._x_speed, self._y_speed = self._pattern(self, dimensions, dt, self._pattern_params[0])
        if self._x_speed == None:
            self.despawn(drop_list)
        else:
            self._direction = 0 if self._x_speed == 0 else copysign(1, float(self._x_speed))
            self._x += self._x_speed * dt
            self._y += self._y_speed * dt
        self.center = self.get_center()

    def _attack(self, projs):
        if self.wait_to_shoot:
            if self._x_speed != 0 or self._y_speed != 0:
                return
        if self._x_speed is None:
            return
        shot_time = pygame.time.get_ticks()
        # self.shot_time should be set in the loader
        if shot_time - self.shot_time >= 1000/self.fire_rate:
            if self._projectile == FallingProjectile:
                proj = self._projectile(self._ID, self, self.center[0], self.center[1], self._direction, self._projectile_params[0])
            else:
                proj = self._projectile(self._ID, self, self.center[0], self.center[1], self._projectile_params[0])
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
    def y_speed(self):
        return self._y_speed

    @y_speed.setter
    def y_speed(self, y_speed):
        self._y_speed = y_speed

    @property
    def drops(self):
        return self._drops
    
    @drops.setter
    def drops(self, drops):
        self._drops = drops

    def update(self, projs, drop_list, screen, dt):
        if self.health < 0:
            if self.last_collision != None:
                self.last_collision.shooter.kills[0] += 1
            self.despawn(drop_list)
        self._move(screen, drop_list, dt)
        self._attack(projs)

    def despawn(self, drop_list):
        super().despawn()

        # spawn some drops
        if self._x_speed is None or self._y_speed is None:
            return
        for d in self._drops:
            drop_params = [float(i) for i in d[1:]]
            drop = entities.drop_types[d[0]](self._x, self._y, drop_params)
            drop.width = 20
            drop.height = 20
            drop_list.append(drop)
            drop.in_list = drop_list
            

class Boss(Entity):
    def __init__(self, ID, patterns, projs):
        """ 
        patterns/projectiles are lists of types, and
        pattern_params/projectile_params are lists of lists of parameters
        """
        super().__init__(ID)
        self._patterns = patterns
        self._pattern_params = None
        self._projectiles = projs
        self._projectile_params = None

        self._health_checkpoint = 0
        self._healths = []
        self._max_health = 0
        self._pattern = self._patterns[0]
        self._projectile = self._projectiles[0]
        self._current = 0

        self._x_speed = None
        self._y_speed = None

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        self._pattern = pattern

    @property
    def patterns(self):
        return self._patterns
    
    @patterns.setter
    def patterns(self, patterns):
        self._patterns = patterns

    @property
    def pattern_params(self):
        return self._pattern_params  

    @pattern_params.setter
    def pattern_params(self, params):
        self._pattern_params = params
    
    @property
    def projectiles(self):
        return self._projectiles

    @projectiles.setter
    def projectiles(self, projs):
        self.projectiles = projs

    @property
    def projectile_params(self):
        return self._projectile_params

    @projectile_params.setter
    def projectile_params(self, params):
        self._projectile_params = params

    @property
    def x_speed(self):
        return self._x_speed

    @x_speed.setter
    def x_speed(self, x_speed):
        self._x_speed = x_speed

    @property
    def y_speed(self):
        return self._y_speed

    @y_speed.setter
    def y_speed(self, y_speed):
        self._y_speed = y_speed

    @property
    def drops(self):
        return self._drops
    
    @drops.setter
    def drops(self, drops):
        self._drops = drops

    def _move(self, screen, dt):
        self._x_speed, self._y_speed = self._pattern(self, screen, dt, self._pattern_params[self._current])
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
                proj = self._projectile(self._ID, self, self.center[0], self.center[1], self._direction, self._projectile_params[self._current])
            else:
                proj = self._projectile(self._ID, self, self.center[0], self.center[1], self._projectile_params[self._current])
            projs.append(proj)
            proj.in_list = projs
            self.shot_time = shot_time

    def update(self, projs, drops, dimensions, dt):
        if self._healths == []:
            self._healths = [self.health-self.health/len(self._patterns)*i for i in range(1, len(self._patterns))] + [0]
        if self.health < 0:
            if self.last_collision != None:
                self.last_collision.shooter.kills[0] += 1
            self.despawn(drops)
        elif self.health < self._healths[self._health_checkpoint]:
            self.switch_pattern()
            self._health_checkpoint += 1
        self._move(dimensions, dt)
        self._attack(projs)

    def switch_pattern(self):
        self._current += 1
        self._pattern = self._patterns[self._current]
        self._projectile = self._projectiles[self._current]
        self._x_speed = None # IT'S RIGHT HERE

    def despawn(self, drops):
        super().despawn()

        # spawn some drops
        for d in self._drops:
            drop_params = [float(d[i]) for i in range(1, len(d))]
            drop = entities.drop_types[d[0]](self._x, self._y, drop_params)
            drop.width = 20
            drop.height = 20
            drops.append(drop)
            drop.in_list = drops

entities.entity_types["Enemy"] = Enemy
entities.entity_types["Boss"] = Boss