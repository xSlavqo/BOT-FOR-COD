def building_print(variable_manager, queue_manager):
    # Pobieranie aktualnego stanu buildings z variable_manager
    buildings = variable_manager.variables.get('buildings', {})
    print(buildings)

    # Sprawdzanie i aktualizowanie poziomów budynków
    if "center" in buildings and buildings["center"].level >= 3:
        buildings["vest"].unlocked = True
    if "center" in buildings and buildings["center"].level >= 5:
        buildings["labo"].unlocked = True
        buildings["cav"].unlocked = True
    if "center" in buildings and buildings["center"].level >= 6:
        buildings["arch"].unlocked = True
    if "center" in buildings and buildings["center"].level >= 16:
        buildings["cele"].unlocked = True

    # Wysyłanie zaktualizowanych danych do kolejki variable_queue
    queue_manager.put('variable', ('buildings', buildings))
