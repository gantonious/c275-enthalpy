import pygame
from entities.individuals import *

# import all interfaces for GUI to run
import interfaces
from interfaces.main_game import Main_Game
from interfaces.legacy_game import Legacy_Game
from interfaces.main_menu import Main_Menu
from interfaces.pause_menu import Pause_Menu
from interfaces.level_select import Level_Select
from interfaces.level_clear import Level_Clear

class GUI:
    """
    GUI is Kami-sama

    Also GUI handles running interfaces such as menus or gameplay. It will run
    the interfaces with top priorty as indicated by the last interface in interfaces,
    when the GUI runs out of interfaces to run, application runtime ends.

    but yeah GUI is Kami-sama
    """

    BLACK    = (   0,   0,   0)
    WHITE    = ( 255, 255, 255)
    RED      = ( 255,   0,   0)
    YELLOW   = ( 255, 255,   0)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.interfaces = []
        self.reset()

    def reset(self):
        """
        Resets GUI screen and registered players
        """
        # reset pygame
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.clock = pygame.time.Clock()

        # reset joysticks/players
        self.players = []
        pygame.joystick.quit()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            player = Player(len(self.players), joystick)
            self.players.append(player)
            player.in_list = self.players

            if (player.get_init() == False):
                self.players.remove(player) # joystick init failed, drop self.player

    def add_interface(self, interface):
        self.interfaces.append(interface)

    def pop_interface(self):
        if self.interfaces:
            return self.interfaces.pop()
        return None

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_icon(self, icon):
        pygame.display.set_icon(icon)

    def run(self):
        """
        Runs gui, updates interface with most priorty, aka last interface in interfaces
        Ends runtime when the gui runs out of interfaces
        """
        alive = True
        last_time = 0
        dt = 0

        while alive:
            if self.interfaces == []:
                alive = False
                continue

            now = pygame.time.get_ticks()
            dt = (now - last_time) / 1000 # in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # If user clicked close
                    alive = False

            interface_status = self.interfaces[-1].update(dt)
            self.interfaces[-1].draw(self.screen, clock=self.clock)

            # handdles changing interfaces, also handles the threads of each interface
            # as the user changes interface
            if interface_status != True:
                if interface_status[0] > 0:
                    for i in range(interface_status[0]):
                        self.interfaces[-1].kill_thread()
                        self.pop_interface()
                # load new interface if specified
                if interface_status[1] != None:
                    if interface_status[0] == 0:
                        # if we didnt kill previous interface, pause its thread
                        self.interfaces[-1].pause_thread()
                    self.add_interface(interfaces.interface_types[interface_status[1]](self.players, self.width, self.height, interface_status[2]))
                if self.interfaces != []:
                    # resume thread of interface with current priority
                    self.interfaces[-1].resume_thread()

            last_time = now
            self.refresh()

        # kills all lingering threads in preperation for ending runtime
        for interface in self.interfaces:
            interface.kill_thread()

        pygame.quit()
        
    def refresh(self):
        pygame.display.flip()
        self.clock.tick(120)