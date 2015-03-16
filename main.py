import pygame, sys
from individuals import *
from gui import *
from threading import Thread

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)

# Set the width and height of the screen [width,height]

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

argv = sys.argv[1:]
if len(argv) > 1:
    SCREEN_SIZE = (int(argv[0]), int(argv[1]))
else:
    SCREEN_SIZE = (1280, 720)

pygame.init()
 
screen = pygame.display.set_mode(SCREEN_SIZE)

main_gui = GUI(*SCREEN_SIZE)

pygame.display.set_caption("PvPy")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# these will eventually be automated
boss = Boss(2, 1000, 0)
boss.health = 1000
boss.width = 40
boss.height = 40
boss.x = 200
boss.y = 40
boss.hitbox = 40

enemy = Enemy(2, 0, 1000, border)
enemy.health = 100
enemy.width = 20
enemy.height = 20
enemy.x = 600
enemy.y = 200
enemy.hitbox = 20

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

last_time = pygame.time.get_ticks()
# -------- Main Program Loop -----------
while done==False:
    now = pygame.time.get_ticks()
    dt = (now - last_time) / 1000 # in seconds
    # print(dt)

    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    screen.fill(WHITE)
    textPrint.reset()
    textPrint.print(screen, "Number of projs: {}".format(len(projs)))
    textPrint.print(screen, "Boss health: {}".format(boss.health))
    textPrint.print(screen, "FPS: {}".format(clock.get_fps()))
    

    for player in enumerate(players):
        player[1].update(projs, screen, dt)
        main_gui.draw_rect(player[1])
        main_gui.draw_hit_box(player[1])
        textPrint.print(screen, "Player {} health: {}".format(player[0] + 1, player[1].health))

    boss.update(projs, screen, dt)
    main_gui.draw_rect(boss)
    enemy.update(projs, screen, dt)

    for proj in projs:
        if proj.on_screen(screen):
            proj.update(screen, dt)
            proj.collide(boss)
            for player in players:
                proj.collide(player)
            main_gui.draw_rect(proj)
        else:
            projs.remove(proj) # drop off proj pointer

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Go ahead and update the screen with what we've drawn.
    # pygame.display.flip()

    main_gui.refresh()

    # Limit to 120 frames per second
    clock.tick(120)

    last_time = now
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()