# legions.py

class Legions:
    def __init__(self, name):
        self.name = name       # Nazwa legionu
        self.status = None     # Domyślny status ustawiony na None
        self.region = None     # Region legionu, początkowo None
        self.set_region()      # Ustawienie regionu na podstawie nazwy legionu
    
    def set_region(self):
        # Przypisanie regionów na podstawie nazwy
        if self.name == "1":
            self.region = (1791, 187, 116, 77)
        elif self.name == "2":
            self.region = (1761, 273, 144, 69)
        elif self.name == "3":
            self.region = (1744, 350, 130, 74)
        elif self.name == "4":
            self.region = (1734, 437, 124, 69)
        elif self.name == "5":
            self.region = (1736, 518, 124, 65)
        else:
            self.region = None  # Na wypadek, gdyby nazwa była inna