import time
from building_menager.building import Building
from building_menager.building_logic import check_lvl

def building_create(variable_manager, variable_queue):
    if 'buildings' not in variable_manager.variables:
        building_names = ["center", "buildings", "labo", "vest", "arch", "inf", "cav", "cele"]
        buildings = {}

        for name in building_names:
            buildings[name] = Building(name=name)
        
        variable_queue.put(('buildings', buildings))
    return

def chceck_unlock(variable_manager, variable_queue):
    time.sleep(1)
    if 'buildings' not in variable_manager.variables:
        raise ValueError("Buildings nie zostały jeszcze utworzone!")
    
    buildings = variable_manager.variables['buildings']
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


def building_main(variable_manager, variable_queue):
    building_create(variable_manager, variable_queue)
    chceck_unlock(variable_manager, variable_queue)