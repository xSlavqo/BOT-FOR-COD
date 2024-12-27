# utils/buildings/read_position.py

import os
import json

def read_position(buildings):
    main_project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    filename = os.path.join(main_project_path, "config.json")

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Plik konfiguracyjny {filename} nie istnieje.")

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    positions = {}
    for building in buildings:
        if building in data:
            positions[building] = data[building]
        else:
            raise KeyError(f"Nie znaleziono koordynatów dla budynku: {building}")

    return positions
