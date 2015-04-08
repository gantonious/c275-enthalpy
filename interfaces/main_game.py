import pygame, sys
from threading import Thread
from entities.individuals import *
from quadtree import Quadtree
from loader import *
import interfaces
from interfaces.interface import Interface
from drawing import *
from textprint import TextPrint

class Main_Game(Interface):
    def __init__(self, players, width, height, params):
        self.projs = []
        self.enemies = []
        self.drops = []
        super().__init__(players, width, height, params)
        self.printer = TextPrint()
        self.play_area = [0, 0, self.width, self.height*0.9]
        self.players = params[0]
        self.level = params[1]
        self.reset()

    def reset(self):
        x_spacing = self.width * 0.05

        for player in enumerate(self.players):
            player[1].health = 100
            player[1].max_health = 100
            player[1].width = 30
            player[1].height = 30
            player[1].hitbox = 8  
            player[1].x = (self.width - len(self.players) * player[1].width - (len(self.players) - 1) * x_spacing) / 2 + player[0] * (player[1].width + x_spacing)
            player[1].y = 600

        self.thread = Thread(target=self.loader_init)
        self.loaded = False
        self.loader = Loader()
        self.proj_tree = Quadtree(*self.play_area)

    def loader_init(self):
        self.loader.interface = self
        self.loader.players = self.players
        self.loader.enemies = self.enemies
        self.loader.load(self.level)

    def update(self, dt):
        """
        Runs all the logic for the current frame
        """

        if not self.thread.is_alive() and not self.loaded:
            self.thread.start()
            self.loaded = True

        self.proj_tree.clear()

        for player in enumerate(self.players):
            player[1].update(self.projs, self.play_area, dt)

        for enemy in self.enemies:
            enemy.update(self.projs, self.drops, self.play_area, dt)

        # update projectiles and insert them into the tree
        for proj in self.projs:
            proj.update(self.play_area, dt)
            self.proj_tree.insert(proj)

        # run collisions on projectiles that have a high chance of colliding with enemy
        for enemy in self.enemies:
            for proj in self.proj_tree.get_objects(enemy):
                proj.collide(enemy)

        # run collisions on projectiles that have a high chance of colliding with player
        for player in self.players:
            for proj in self.proj_tree.get_objects(player):
                proj.collide(player)
            for drop in self.drops:
                drop.collide(player)

        if not self.enemies:
            self.loader.set_clear(True)

        if self.players[0].health < 0:
            return (1, "main_menu", [])
            
        if self.players[0].get_debounced_input(6):
            return (0, "pause_menu", [])

        if self.loader.finished and self.enemies == [] or self.players[0].get_debounced_input(7):
            return (1, "level_clear", [self.players, self.loader.level_name, self.loader.next_level])

        return True

    def pause_thread(self):
        if self.thread.is_alive():
            self.loader.paused = True

    def resume_thread(self):
        if self.thread.is_alive():
            self.loader.paused = False

    def kill_thread(self):
        if self.thread.is_alive():
            self.loader.game_is_running = False

    def draw(self, screen, clock=None):
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255 ,255 ,255), self.play_area)

        for player in enumerate(self.players):
            draw_entity(screen, player[1])
            draw_hit_box(screen, player[1])
            draw_health_bar(screen, player[1])

        for enemy in self.enemies:
            draw_entity(screen, enemy)
            draw_health_bar(screen, enemy)

        for proj in self.projs:
            draw_entity(screen, proj)

        for drop in self.drops:
            if not drop.used:
                draw_entity(screen, drop)
            else:
                drop.update()

        self.printer.reset()
        self.printer.print_text(screen, "FPS: {}".format(clock.get_fps()), (0, 0, 0))

interfaces.interface_types["main_game"] = Main_Game