import time
from building_menager.building import Building
from building_menager.building_operations import *
from building_menager.building_queue import *

def building_main(variable_manager, variable_queue):
    # Tworzenie budynków
    building_names = ["center", "buildings", "labo", "vest", "arch", "inf", "cav", "cele"]
    buildings = {name: Building(name=name) for name in building_names}
    
    # Sprawdzanie odblokowania
    time.sleep(1)
    check_lvl(buildings["center"])

    if buildings["center"].level >= 3:
        buildings["vest"].unlocked = True
    if buildings["center"].level >= 5:
        buildings["labo"].unlocked = True
        buildings["cav"].unlocked = True
    if buildings["center"].level >= 6:
        buildings["arch"].unlocked = True
    if buildings["center"].level >= 16:
        buildings["cele"].unlocked = True

    # Automatyczne budowanie - Sprawdzanie istnienia kolejek
    if 'queue1' not in variable_manager.variables:
        queue1 = BuildQueue(1)
        variable_manager.variables['queue1'] = queue1
    else:
        queue1 = variable_manager.variables['queue1']

    if 'queue2' not in variable_manager.variables:
        queue2 = BuildQueue(2)
        variable_manager.variables['queue2'] = queue2
    else:
        queue2 = variable_manager.variables['queue2']

    # Kontrolowanie kolejek - Teraz wywołujemy metodę `control_queue`
    queue1.control_queue(buildings["buildings"])
    queue2.control_queue(buildings["buildings"])

    # Wysyłanie do variable_queue
    variable_queue.put(('buildings', buildings))
    variable_queue.put(('queue1', queue1))
    variable_queue.put(('queue2', queue2))
