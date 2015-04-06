import pygame
from entities.individuals import *

# import all interfaces for GUI to run
import interfaces
from interfaces.main_game import Main_Game
from interfaces.main_menu import Main_Menu

class GUI:
    """
    GUI is Kami-sama

    Also GUI handles running interfaces such as menus or gameplay. It will run
    the interfaces with top priorty as indicated by the last interface in interfaces,
    when the GUI runs out of interfaces to run, application runtime ends.

    but yeah GUI is Kami-sama
    """

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

        # IDs 0 and 1 are reserved for self.players for the time being
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            player = Player(i, joystick)
            # 100, 30, 30, 240, 600, 4, 5, RED
            self.players.append(player)
            player.in_list = self.players

            if (player.get_init == 0):
                self.players.remove(player) # joystick init failed, drop self.player

    def add_interface(self, interface):
        self.interfaces.append(interface)

    def pop_interface(self):
        if self.interfaces:
            return self.interfaces.pop()
        return None

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

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

            # EVENT PROCESSING STEP
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    alive = False # Flag that we are done so we exit this loop

            interface_status = self.interfaces[-1].update(self.screen, dt)
            self.interfaces[-1].draw(self.screen)

            # handdles changing interfaces, also handles the threads of each interface
            # as the user changes interface
            if interface_status != True:
                if not interface_status[0]:
                    # kill current interface
                    self.interfaces[-1].kill_thread()
                    self.pop_interface()
                # load new interface if specified
                if interface_status[1] != None:
                    if interface_status[0]:
                        # if we didnt kill previous interface, pause its thread
                        self.interfaces[-1].pause_thread()
                    self.add_interface(interfaces.interface_types[interface_status[1]](self.players, self.width, self.height))
                if self.interfaces != []:
                    # resume thread of interface with current priority
                    self.interfaces[-1].resume_thread()

            last_time = now
            self.refresh()

        pygame.quit()
        
    def refresh(self):
        pygame.display.flip()
        self.clock.tick(120)
