import pygame
from individuals import *
import time
from threading import Thread

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

# Set the width and height of the screen [width,height]
SCREEN_SIZE = [1200, 800]

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

def refresh_joysticks():
    pygame.joystick.quit()
    pygame.joystick.init()

pygame.init()
 
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption("PvPy")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
boss = Boss(2, 30, 0)
boss.health = 1000
boss.width = 40
boss.height = 40
boss.x = 200
boss.y = 40
boss.hitbox = 40

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()
projs = []
players = []

joystick_count = pygame.joystick.get_count()

textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
textPrint.indent()

# IDs 0 and 1 are reserved for players for the time being
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    player = Player(i, joystick)
    # 100, 30, 30, 240, 600, 4, 5, RED
    player.health = 100
    player.width = 30
    player.height = 30
    player.hitbox = 5
    if player.ID == 0:
        player.x = 400
        player.y = 600
    if player.ID == 1:
        player.x = 800
        player.y = 600
    players.append(player)

    if (player.get_init == 0):
        players.remove(player) # joystick init failed, drop player

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    screen.fill(WHITE)
    textPrint.reset()

    textPrint.print(screen, "Number of projs: {}".format(len(projs)))
    textPrint.print(screen, "Boss health: {}".format(boss.health))
    

    for player in enumerate(players):
        player[1].update(projs, screen)
        textPrint.print(screen, "Player {} health: {}".format(player[0] + 1, player[1].health))
    
    boss.update(projs, screen)


    for proj in projs:
        if proj.on_screen(screen):
            proj.update(screen)
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