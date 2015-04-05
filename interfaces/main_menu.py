from interfaces.main_game import Main_Game
from interfaces.interface import Interface

class Main_Menu(Interface):
    def __init__(self, gui):
        super().__init__(gui)

    def update(self, screen, dt):
        if self.players:
            if self.players[0].get_input()[4]:
                self.gui.interfaces.remove(self)
                self.gui.interfaces.append(Main_Game(self.gui))

    def draw(self, screen):
        screen.fill(self.gui.WHITE)