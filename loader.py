from threading import Thread

class Loader(Thread):

    def run(self, level):
        with open(level, 'r') as lvl:
            load_header(lvl)
            while True:
                if load_next(lvl) is None:
                    break

    def load_header(self, lvl):
        # load assets and important information

    def load_next(self):
        # load enemies as they happen