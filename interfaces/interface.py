class Interface:
    def __init__(self, players, width, height):
        self.players = players
        self.width = width
        self.height = height

    def reset(self):
        pass

    def pause_thread(self):
        pass

    def resume_thread(self):
        pass

    def kill_thread(self):
        pass

    def update(self, screen, dt):
        """
        Runs all the logic for the current frame

        Returns: 

        True - Keep this interface alive and do nothing else
        (Bool, Interface) - Add interface Interface with highest priority, 
        Bool indicates whether to keep current Interface alive or not
        """
        pass
        
    def draw(self, screen):
        """
        Draws Interface to the screen
        """
        pass