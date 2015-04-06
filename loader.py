import entities, time

class Loader:
    def __init__(self):
        self._keep_going = True
        self.finished = False
        self.players = None # pass the list of players to loader pls
        self.enemies = None # also the list of enemies pls thx
        self.interface = None # one more thing
        self.game_is_running = True

    def set_clear(self, boolean):
        self._keep_going = boolean

    def get_clear(self):
        return self._keep_going

    def load(self, level):
        with open(level, 'r') as lvl:
            self.load_header(lvl, self.interface)
            while self.game_is_running:
                if self.get_clear() and self.load_next(lvl) is None:
                    break
        self.finished = True

    def load_header(self, lvl, interface):
        # load assets and important information

        # level number
        line = lvl.readline()
        while line.find("Level: ") < 0:
            line = lvl.readline()
            if line == "":
                raise Exception("Expected level number")

        # Get the level number
        line = line.lstrip("Level: ")
        self.interface.level_num = int(line)

        # level name
        line = lvl.readline()
        while line.find("Name: ") < 0:
            line = lvl.readline()
            if line == "":
                raise Exception("Expected level name")

        # Get the level name
        line = line.lstrip("Name: ")
        self.interface.level_name = line

        # enemies block
        line = lvl.readline()
        while line.find("Enemies:") < 0:
            line = lvl.readline()
            if line == "":
                raise Exception("Expected enemies start")

    def load_next(self, lvl):
        # load enemies as they happen
        # return 0 if we still have stuff to load, return None if done
        line = lvl.readline()
        while line.find("Enemies end") < 0:
            if line == "\n":
                line = lvl.readline()
                continue

            line = line.rstrip()
            if line == "Clear":
                self.set_clear(False)
                return 0

            line = line.split(' ')

            # delay line[1] ms
            if line[0] == "Delay":
                time.sleep(int(line[1])/1000)
                line = lvl.readline()
                continue

            # ignore line
            if line[0] == "#":
                line = lvl.readline()
                continue

            # Enemy x y width height health hitbox fire_rate
            if len(line) != 8:
                raise Exception("Invalid enemy definition: {}".format(str(line)))

            move_line = lvl.readline()
            move_line = move_line.rstrip()
            move_line = move_line.lstrip("*")
            move_line = move_line.split(' ')
            if move_line[0].find("*") == 0:
                raise Exception("Invalid/no movement definition: {}".format(str(move_line)))

            proj_line = lvl.readline()
            proj_line = proj_line.rstrip()
            proj_line = proj_line.lstrip("**")
            proj_line = proj_line.split(' ')
            if proj_line[0].find("*") == 0:
                raise Exception("Invalid/no projectile definition: {}".format(str(proj_line)))

            drop_list = []
            drop_line = lvl.readline()
            while drop_line is not "\n":
                drop_line = drop_line.rstrip()
                drop_line = drop_line.lstrip("***")
                drop_line = drop_line.split(' ')
                if drop_line[0].find("*") == 0:
                    raise Exception("Invalid/no drop definition: {}".format(str(drop_line)))
                drop_list.append(drop_line)
                drop_line = lvl.readline()

            # create entity with the defined properties
            entity = entities.entity_types[line[0]] \
                    (2, entities.pattern_types[move_line[0]], \
                    entities.entity_types[proj_line[0]])
            entity.x = int(line[1])
            entity.y = int(line[2])
            entity.health = int(line[3])
            entity.width = int(line[4])
            entity.height = int(line[5])
            entity.hitbox = int(line[6])
            entity.fire_rate = int(line[7])
            entity.shot_time = 0 # shots per second
            entity.pattern_params = [float(move_line[i]) for i in range(1, len(move_line))]
            entity.projectile_params = [float(proj_line[i]) for i in range(1, len(proj_line)-1)]
            # oh man i am not good with computer pls to help
            # conditional for targeting projectiles
            if entities.entity_types[proj_line[0]].targets:
                if len(self.players) > int(proj_line[-1]):
                    entity.projectile_params.append(self.players[int(proj_line[-1])])
                else:
                    entity.projectile_params.append(None)
            else:
                entity.projectile_params.append(float(proj_line[-1]))
            entity.center = entity.get_center()
            entity.drops = drop_list

            self.enemies.append(entity)
            entity.in_list = self.enemies
            return 0

        return None
