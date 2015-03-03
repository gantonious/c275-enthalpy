import pygame
import time
from threading import Thread

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10

class Projectile:
    def __init__(self, x, y, x_speed, y_speed, damage, color, ID):
        self._width = 5
        self._height = 5
        self._x = x
        self._y = y
        self._x_speed = x_speed
        self._y_speed = y_speed
        self._damage = damage
        self._state = 0 # 0 offscreen 1 on
        self._color = color
        self._ID = ID
        self._move()


    def _move(self):
        self._x += self._x_speed
        self._y += self._y_speed
        pygame.draw.rect(screen, self._color, [self._x, self._y, self._width, self._height], 2)
        if (self._x + self._width > 0 and self._x < 500) and \
            (self._y + self._height > 0 and self._y < 700):
            self._state = 1
        else:
            self._state = 0
        if (int(self._x_speed) == 0 and int(self._y_speed) == 0):
            self._state = 0 # prepare for garbage collection

    def collide(self, target):
        if target.get_ID() == self._ID:
            return 0
        coords = target.get_coords()
        if (self._x + self._width > coords[0] and \
            self._x < coords[0] + coords[2] and \
            self._y + self._height > coords[1] and \
            self._y < coords[1] + coords[3]):
            self._state = 0
            target.update_health(-1*self._damage)
            return 1
        return 0

    def on_screen(self):
        return self._state

    def update(self):
        self._move()

class Player:
    def __init__(self, joystick):
        """
        P
        """
        self._health = 100
        self._damage = 5
        self._width = 30
        self._height = 30
        self._x = 240
        self._y = 600
        self._hitbox_size = 4
        self._ID = 1
        self._color = RED
        self._sensitivity = 3
        self._shoot_sensitivity = 30
        self._slowdown = 1
        self._threshold = 0.08
        self._joystick = joystick # grabs this players joystick object
        joystick.init() # initializes joysticks
        self._map = []
	
    def get_init(self):
        status = self._joystick.get_init()

        if status == 0:
            self._joystick.quit()

        return status

    def map_joystick(self):
        if self._joystick.get_name() == "Wireless Controller":
            self._map = [0, 1, 2, 3, 4]
        elif self._joystick.get_name() == "PLAYSTATION(R)3 Controller":
            self._map = [0, 1, 2, 3, 11]
        else:
            self._map = [0, 1, 2, 3, 11] # default mapping


    def _draw(self):
        pygame.draw.rect(screen, self._color, \
            [self._x, self._y, self._width, self._height], 2)
        pygame.draw.rect(screen, self._color, \
            [self._x + (self._width - self._hitbox_size)/2, \
            self._y + (self._height - self._hitbox_size)/2, \
            self._hitbox_size, self._hitbox_size], 2)

    def _move(self):
        joy_input = self._get_input()

        # number crunching, these magic numbers are the screen dimensions ill get rid of them soon

        if abs(joy_input[0]) > self._threshold:
            self._x += (self._sensitivity - (self._slowdown*joy_input[4]))*joy_input[0]
            if self._x < 0:
                self._x = 0
            elif self._x + self._width > 500:
                self._x = 500 - self._width

        if abs(joy_input[1]) > self._threshold:
            self._y += (self._sensitivity - (self._slowdown*joy_input[4]))*joy_input[1]
            if self._y < 0:
                self._y = 0
            elif self._y + self._height > 700:
                self._y = 700 - self._height

        self._draw()


    def _shoot(self, proj_container):
        joy_input = self._get_input()

        if abs(joy_input[2]) > self._threshold or abs(joy_input[3]) > self._threshold:
            proj_container.append(Projectile(self._x + self._width / 2 - 2, self._y + self._height/2 - 2, \
                    self._shoot_sensitivity*joy_input[2], self._shoot_sensitivity*joy_input[3], \
                    self._damage, self._color, self._ID))

    def _get_input(self):
        return (self._joystick.get_axis(self._map[0]), \
                self._joystick.get_axis(self._map[1]), \
                self._joystick.get_axis(self._map[2]), \
                self._joystick.get_axis(self._map[3]), \
                self._joystick.get_button(self._map[4]))

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

    def update(self, proj_container):
        self._move()
        self._shoot(proj_container)

class Boss:
    def __init__(self):
        self._health = 1000
        self._width = 40
        self._height = 40
        self._x = 200
        self._y = 40
        self._hitbox_size = 40
        self._x_speed = 30
        self._y_speed = 0
        self._state = (0, 0)
        self._moves = [(0, 0), (2, 0), (0, 0)] # tuples containg move and countdown
        self._ID = 0
        self._move()

    def _move(self):
        if self._x < 0:
            self._x_speed = 30
        elif self._x > 500:
            self._x_speed = -30
        self._x += self._x_speed
        self._y += self._y_speed
        pygame.draw.rect(screen, BLACK, [self._x, self._y, self._width, self._height], 2)

    def _attack(self, proj_container):
        """
        """
        if time.time() - self._moves[0][0] > self._moves[0][1]:
            self._moves[0] = (.5, time.time())
            i = 0
            x = -1.0
            y = -1.0
            while(i < 20):
                proj_container.append(Projectile(self._x + self._width / 2, self._y + self._height / 2, x*3, y*3, 10, BLACK, 0))
                proj_container.append(Projectile(self._x + self._width / 2, self._y + self._height / 2, x*-3, y*3, 10, BLACK, 0))
                x += 0.1
                y += 0.1
                i += 1
        if time.time() - self._moves[1][0] > self._moves[1][1]:
            self._moves[1] = (2.5, time.time())
            i = 0
            x = -1.0
            y =  0.0
            while(i < 20):
                proj_container.append(Projectile(self._x + self._width / 2, self._y + self._height / 2, x*3, y*3, 10, BLACK, 0))
                proj_container.append(Projectile(self._x + self._width / 2, self._y + self._height / 2, x*-3, y*3, 10, BLACK, 0))
                x += 0.1
                y += 0.1
                i += 1

        if time.time() - self._moves[2][0] > self._moves[2][1]:
            self._moves[2] = (0.2, time.time())
            i = 0
            x = -1.0
            y =  0.0
            while(i < 20):
                proj_container.append(Projectile(self._x + self._width / 2, self._y + self._height / 2, x*3, y*3, 10, BLACK, 0))
                proj_container.append(Projectile(self._x + self._width / 2, self._y + self._height / 2, x*-3, y*3, 10, BLACK, 0))
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

    def update(self, proj_container):
        self._move()
        self._attack(proj_container)

    

pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
boss = Boss()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()
projs = []
players = []

joystick_count = pygame.joystick.get_count()

textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
textPrint.indent()

for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    player = Player(joystick)
    players.append(player)

    if (player.get_init == 0):
        players.remove(player)

    player.map_joystick()
        
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    screen.fill(WHITE)
    textPrint.reset()

    textPrint.print(screen, "Number of projs: {}".format(len(projs)))
    textPrint.print(screen, "Boss health: {}".format(boss.get_health()))
    
    for player in enumerate(players):
        player[1].update(projs)
        textPrint.print(screen, "Player {} health: {}".format(player[0] + 1, player[1].get_health()))
    
    boss.update(projs)

    for proj in projs:
        if proj.on_screen():
            proj.update()
            proj.collide(boss)
            for player in players:
                proj.collide(player)
        else:
            projs.remove(proj) # drop off proj pointer

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    # Limit to 120 frames per second
    clock.tick(120)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()