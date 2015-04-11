import pygame, sys
from threading import Thread
from entities.individuals import *
from quadtree import Quadtree
from loader import *
from elements import *
import interfaces
from interfaces.interface import Interface
from drawing import *

class Legacy_Game(Interface):
    def __init__(self, players, width, height, params):
        self.projs = []
        super().__init__(players, width, height, params)
        self.play_area = [0, 0, self.width, self.height*0.9]
        self.players = params[0]
        pygame.mixer.stop()
        self.background_music = pygame.mixer.Sound(file = "assets/audio/main game.wav")
        self.background_music.play(loops=-1, fade_ms=2000)
        self.reset()

    def reset(self):
        x_spacing = self.width * 0.05

        for player in enumerate(self.players):
            player[1].health = 100
            player[1].max_health = 100
            player[1].width = 30
            player[1].height = 30
            player[1].hitbox = 8  
            player[1].proj_size = 10
            player[1].invuln_active = False
            player[1].x = (self.width - len(self.players) * player[1].width - (len(self.players) - 1) * x_spacing) / 2 + player[0] * (player[1].width + x_spacing)
            player[1].y = 600

        self.alive_players = self.players[:]
        self.proj_tree = Quadtree(self.play_area[0], self.play_area[1], self.play_area[2], self.play_area[3], 3, 1)

        self.status_bar = []
        x_spacing = 20
        status_bar_width = min(self.width * 0.18, (self.width - (len(self.players) - 1) * x_spacing))
        status_bar_height = self.height - self.play_area[3]
        status_bar_x = (self.width - len(self.players) * status_bar_width - (len(self.players) - 1) * x_spacing) / 2
        status_bar_y = self.height - status_bar_height

        for player in enumerate(self.players):
            self.status_bar.append(CharacterStatusBar(status_bar_x + player[0] * (x_spacing + status_bar_width), status_bar_y, status_bar_width, status_bar_height, player[1]))


    def update_alive_players(self):
        for player in self.alive_players:
            if player.health <= 0:
                self.alive_players.remove(player)
                if player.last_collision != None:
                    player.last_collision.shooter.kills[1] += 1
                    player.last_collision.shooter.score += 100

    def update(self, dt):
        """
        Runs all the logic for the current frame
        """

        self.proj_tree.clear()

        # update players
        for player in enumerate(self.alive_players):
            player[1].update(self.projs, self.play_area, dt)

        # projectile - projectile collison
        for proj in self.projs:
            proj.update(self.play_area, dt)
            self.proj_tree.insert(proj)
            for other_proj in self.proj_tree.get_objects(proj):
                proj.collide(other_proj)

        # run collisions on projectiles that have a high chance of colliding with player
        for player in self.alive_players:
            for proj in self.proj_tree.get_objects(player):
                proj.collide(player)

        self.update_alive_players()

        if len(self.alive_players) <= 1:
            return (1, "level_clear", [self.players, "Legacy Mode", None, True])
            
        if self.players[0].get_debounced_input(6):
            return (0, "pause_menu", ["Legacy Mode"])

        return True

    def draw(self, screen, clock=None):
        screen.fill((255, 255, 255))

        for player in enumerate(self.alive_players):
            draw_entity(screen, player[1])
            draw_hit_box(screen, player[1])
            draw_health_bar(screen, player[1])

        for proj in self.projs:
            draw_entity(screen, proj)

        self.proj_tree.draw(screen)

        for player_status in self.status_bar:
            player_status.draw(screen)


interfaces.interface_types["legacy_game"] = Legacy_Game