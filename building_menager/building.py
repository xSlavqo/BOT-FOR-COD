from tools.buildings_config import load_building_coordinates

class Building:
    positions = load_building_coordinates()

    def __init__(self, name):
        self.name = name
        if name in ["center", "buildings"]:
            self.unlocked = True
        else:
            self.unlocked = None
        self.position_x, self.position_y = self.positions.get(self.name, (0, 0))
        self.level = None
        self.level_up = None
        self.work = None

        if name in ['vest', 'arch', 'inf', 'cav', 'cele']:
            self.type = 'train'
        else:
            self.type = None