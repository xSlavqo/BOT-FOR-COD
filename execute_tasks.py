import time
from func_timeout import func_timeout, FunctionTimedOut
from tasks.rss_map import rss_map
from tasks.alliance import ally_help, ally_gifts
from tasks.hospital import hospital
from tasks.cod import cod
from tools.functions import load_settings

# Funkcja opakowująca zadanie opcjonalnym timeoutem
def task_with_optional_timeout(task_func, timeout=None):
    def wrapper():
        if timeout:
            try:
                task_func()
            except FunctionTimedOut:
                raise FunctionTimedOut(f"Zadanie {task_func.__name__} nie zostało ukończone w wyznaczonym czasie.")
        else:
            task_func()
    return wrapper

# Definiowanie grup z funkcjami i ich właściwościami
task_groups = {
    "GENERAL": {
        "cod": (cod, 100, 0, True)  # True oznacza, że jest krytyczne
    },
    "MAPA": {
        "rss_map": (rss_map, 120, 0, False)  # False oznacza, że nie jest krytyczne
    },
    "MIASTO": {
        "hospital": (hospital, 30, 1800, False)
    },
    "MAPA LUB MIASTO": {
        "ally_help": (ally_help, 10, 0, False)
    },
    "SOJUSZ": {
        "ally_gifts": (ally_gifts, 240, 1800, False)
    }
}

# Przekształcanie zadań w task_groups, aby uwzględniały timeout i interval
for group, tasks in task_groups.items():
    for task_name, (func, timeout, interval, critical) in tasks.items():
        tasks[task_name] = (task_with_optional_timeout(func, timeout), interval, critical)

last_execution_time = {}

# Funkcja sprawdzająca, czy zadanie może zostać wykonane
def can_execute_task(task_name, interval, current_time):
    return current_time - last_execution_time.get(task_name, 0) >= interval

# Funkcja aktualizująca czas ostatniego wykonania zadania
def update_last_execution_time(task_name, current_time):
    last_execution_time[task_name] = current_time

# Główna funkcja wykonująca zadania
def execute_tasks():
    config = load_settings()
    current_time = time.time()

    # Wykonywanie zadań
    for group_name, tasks in task_groups.items():
        for task_name, (task_func, interval, critical) in tasks.items():
            if config.get(task_name, "false").lower() == "true":
                if not can_execute_task(task_name, interval, current_time):
                    continue

                if task_func:
                    try:
                        task_func()
                        update_last_execution_time(task_name, current_time)
                        time.sleep(2)
                    except Exception as e:
                        print(f"Zadanie {task_name} nie powiodło się: {e}")
                        if critical:
                            print(f"Krytyczne zadanie {task_name} nie powiodło się, zatrzymanie wykonywania.")
                            return  # Przerywamy dalsze wykonywanie, gdy zadanie krytyczne nie powiedzie się