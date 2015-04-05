class Interface:
    def __init__(self, gui):
        self.gui = gui
        self.reset()

    def reset(self):
        self.players = self.gui.players

    def kill_thread(self):
        pass

    def update(self, screen, dt):
        pass
        
    def draw(self, screen):
        pass