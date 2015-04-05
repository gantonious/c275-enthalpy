import interfaces
from interfaces.interface import Interface

class Main_Menu(Interface):
    def __init__(self, gui):
        super().__init__(gui)

    def update(self, screen, dt):
        if self.players:
            if self.players[0].get_input()[5]:
            	return (False, "main_game")
                # self.gui.interfaces.remove(self)
                # self.gui.interfaces.append(Main_Game(self.gui))
            if self.players[0].get_input()[4]:
            	return (False, None)

        return True

    def draw(self, screen):
        screen.fill(self.gui.WHITE)
        self.gui.refresh()

interfaces.interface_types["main_menu"] = Main_Menu