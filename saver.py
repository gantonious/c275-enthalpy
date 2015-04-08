import os.path, tkinter
from tkinter.filedialog import askopenfilename

class Saver:
    def __init__(self):
        self.save_exists = False
        self.save_file = None

    def find_save(self):
        root = tkinter.Tk()
        root.withdraw()
        root.filename = askopenfilename(initialdir = "saves", title = "Choose a save", \
                            filetypes = (("save files","*.sav"),("all files","*.*")))
        self.load(root.filename)

    def load(self, save):
        # load all the things
        f = open(save, "r+")
        line = f.readline()
        if line.find(".lvl") < 0:
            raise Exception("Corrupt save!")
        self.save_file = line
        self.save_exists = True

    def save(self, players, level):
        if self.save_exists:
            f = open(self.save_file, "w+") # this should empty the save file by default
            f.write(level)
            f.close()

        count = 0
        while os.path.isfile("saves/{}.sav".format(count)):
            count += 1
        f = open("saves/{}.sav".format(count))
        f.write(level)
        f.close()