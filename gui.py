import pygame
from textprint import TextPrint
from entities.individuals import *

# import all interfaces for GUI to run
import interfaces
from interfaces.main_game import Main_Game
from interfaces.main_menu import Main_Menu

class GUI:
    """
    GUI is Kami-sama
    """
    BLACK    = (   0,   0,   0)
    WHITE    = ( 255, 255, 255)
    RED      = ( 255,   0,   0)

    def __init__(self, width, height):
        pygame.init()
        self._screen = pygame.display.set_mode([width, height])
        self._play_area = [width*0.025, height*0.05, width*0.95, height*0.8]
        self._width = width
        self._height = height
        self.level_num = None
        self.level_name = None
        self.interfaces = []
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
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
    
    def draw_player_status(self, players):
        if not players:
            return

        num_players = len(players)
        spacing = 20
        status_width = min(int(self._width / num_players) - spacing, 200)
        start = int((self._width - status_width*num_players)/ num_players - spacing)
        status_height = int(self._height * 0.125)

        for player in enumerate(players):
            # draws status box
            pygame.draw.rect(self._screen, player[1].color, 
                (start + spacing / 2 + player[0] * (status_width + spacing), 
                self._height - status_height, status_width, status_height))

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def draw_rect(self, entity):
        pygame.draw.rect(self._screen, entity.color, entity.get_position(), 2)

    def draw_hit_box(self, entity):
        pygame.draw.rect(self._screen, entity.color, entity.get_coords(), 2)

    def draw_game_background(self):
        self._screen.fill(GUI.BLACK)
        pygame.draw.rect(self._screen, GUI.WHITE, self._play_area)

    def get_play_area(self):
        return self._play_area

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

            interface_status = self.interfaces[-1].update(self._screen, dt)
            self.interfaces[-1].draw(self._screen)

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
                    self.add_interface(interfaces.interface_types[interface_status[1]](self))
                if self.interfaces != []:
                    # resume thread of interface with current priority
                    self.interfaces[-1].resume_thread()

            last_time = now
            print(self.clock.get_fps())

        if self.interfaces != []:
            self.interfaces[-1].kill_thread()
        
        pygame.quit()
        
    def refresh(self):
        pygame.display.flip()
        self.clock.tick(120)
