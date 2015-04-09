import pygame, sys
from threading import Thread
from entities.individuals import *
from quadtree import Quadtree
from loader import *
import interfaces
from interfaces.interface import Interface
from drawing import *
from textprint import TextPrint

class Legacy_Game(Interface):
    def __init__(self, players, width, height, params):
        self.projs = []
        super().__init__(players, width, height, params)
        self.printer = TextPrint()
        self.play_area = [0, 0, self.width, self.height*0.9]
        self.players = params[0]
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

        self.proj_tree = Quadtree(self.play_area[0], self.play_area[1], self.play_area[2], self.play_area[3], 3, 1)

    def num_players_alive(self):
        num_alive = 0
        for player in self.players:
            if player.health > 0:
                num_alive += 1
        return num_alive

    def update(self, dt):
        """
        Runs all the logic for the current frame
        """

        self.proj_tree.clear()

        # update players
        for player in enumerate(self.players):
            player[1].update(self.projs, self.play_area, dt)

        # projectile - projectile collison
        for proj in self.projs:
            proj.update(self.play_area, dt)
            self.proj_tree.insert(proj)
            for other_proj in self.proj_tree.get_objects(proj):
                proj.collide(other_proj)

        # run collisions on projectiles that have a high chance of colliding with player
        for player in self.players:
            for proj in self.proj_tree.get_objects(player):
                proj.collide(player)

        if self.num_players_alive() <= 1:
            return (1, "main_menu", [])
            
        if self.players[0].get_debounced_input(6):
            return (0, "pause_menu", ["Legacy Mode"])

        return True

    def draw(self, screen, clock=None):
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255 ,255 ,255), self.play_area)

        for player in enumerate(self.players):
            draw_entity(screen, player[1])
            draw_hit_box(screen, player[1])
            draw_health_bar(screen, player[1])

        for proj in self.projs:
            draw_entity(screen, proj)

        self.proj_tree.draw(screen)

        self.printer.reset()
        self.printer.print_text(screen, "FPS: {}".format(clock.get_fps()), (0, 0, 0))

interfaces.interface_types["legacy_game"] = Legacy_Game