class Interface:
    def __init__(self, players, width, height, params):
        self.players = players
        self.width = width
        self.height = height
        self.threshold = 0.08

    def pause_thread(self):
        """
        Pauses all threads of the interface
        """
        pass

    def resume_thread(self):
        """
        Resumes threads of the interface
        """
        pass

    def kill_thread(self):
        """
        Kills all threads of the interface
        """
        pass

    def update(self, dt):
        """
        Runs all the logic for the current frame

        Returns: 

        True - Keep this interface alive and do nothing else
        (Int, Interface, [Prams]) - Add interface Interface with highest priority, 
        Int represents how many interfaces to kill from highest priority to least priority:
        Int = 0 preserves all interfaces
        Int = 1 kills current interface
        Int = 2 kills current and its parent interface and so on...
        Prams - contains any extra paramters needed by GUI to initialize the new interface
        """
        pass
        
    def draw(self, screen, clock=None):
        """
        Draws Interface to the screen
        """
        pass