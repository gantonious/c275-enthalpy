import pygame, sys
from threading import Thread
from entities.individuals import *
from quadtree import Quadtree
from gui import *
from loader import *
from textprint import TextPrint

class Main_Game:
    def __init__(self, gui):
        self.gui = gui
        self.projs = []
        self.enemies = []
        self.players = gui.players
        self.reset()

    def reset(self):
        self.thread = Thread(target=self.loader_init)
        global loaded
        self.loaded = False
        self.loader = Loader()

        self.proj_tree = Quadtree(*self.gui.get_play_area())

    def loader_init(self):
        self.loader.gui = self.gui
        self.loader.players = self.players
        self.loader.enemies = self.enemies
        self.level = "levels/1.lvl"
        self.loader.load(self.level)

    def update(self, screen, dt):
        """
        Runs all the logic for the current frame
        """

        if not self.thread.is_alive() and not self.loaded:
            self.thread.start()
            self.loaded = True

        self.proj_tree.clear()

        for player in enumerate(self.players):
            # gui.draw_rect(player[1])
            # gui.draw_hit_box(player[1])
            player[1].update(self.projs, screen, dt)
            #textPrint.print_text(screen, "Player {} health: {}".format(player[0] + 1, player[1].health))

        for enemy in self.enemies:
            enemy.update(self.projs, screen, dt)
            # gui.draw_rect(enemy)

        for proj in self.projs:
            proj.update(screen, dt)
            self.proj_tree.insert(proj)
            # for enemy in enemies:
            #     proj.collide(enemy)
            # for player in players:
            #     proj.collide(player)
            #     collision += 1
            # gui.draw_rect(proj)

        for enemy in self.enemies:
            for proj in self.proj_tree.get_objects(enemy):
                proj.collide(enemy)

        for player in self.players:
            for proj in self.proj_tree.get_objects(player):
                proj.collide(player)

        if not self.enemies:
            self.loader.set_clear(True)

        # proj_tree.draw_tree(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        # Go ahead and update the screen with what we've drawn.
        # pygame.display.flip()

        # gui.refresh()

    def kill_thread(self):
        if self.thread.is_alive():
            self.loader.game_is_running = False

    def draw(self, screen):
        self.gui.draw_game_background()
        self.gui.draw_player_status(self.players)

        for player in enumerate(self.players):
            self.gui.draw_rect(player[1])
            self.gui.draw_hit_box(player[1])

        for enemy in self.enemies:
            self.gui.draw_rect(enemy)

        for proj in self.projs:
            self.gui.draw_rect(proj)

        self.proj_tree.draw_tree(screen)

        self.gui.refresh()