import time
from func_timeout import func_timeout, FunctionTimedOut
from tasks.rss_map import rss_map
from tasks.alliance import ally_help, ally_gifts
from tasks.hospital import hospital
from tasks.dialogues import dialogues
from tasks.windows_management import cod_run, cod_restart, tv_close
from tools.functions import load_settings

def task_with_optional_timeout(task_func, timeout=None):
    def wrapper():
        if timeout:
            try:
                func_timeout(timeout, task_func)
            except FunctionTimedOut:
                raise FunctionTimedOut(f"Zadanie {task_func.__name__} nie zostało ukończone w wyznaczonym czasie.")
        else:
            task_func()
    return wrapper

# Definiowanie grup z funkcjami i ich właściwościami
task_groups = {
    "GENERAL": {
        "tv_close": (tv_close, 100, 0, True),
        "cod": (cod_run, 100, 0, True)
    },
    "MAPA": {
        "rss_map": (rss_map, 120, 0, False)
    },
    "MIASTO": {
        "hospital": (hospital, 30, 1800, False),
        "dialogues": (dialogues, 120, 0, False)
    },
    "MAPA LUB MIASTO": {
        "ally_help": (ally_help, 10, 0, False)
    },
    "SOJUSZ": {
        "ally_gifts": (ally_gifts, 300, 1800, False)
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
def execute_tasks(queue, stop_event):
    config = load_settings()
    current_time = time.time()

    for group_name, tasks in task_groups.items():
        for task_name, (task_func, interval, critical) in tasks.items():
            task_config = config.get(task_name)

            if task_config is None and critical:
                error = execute_task(task_name, task_func, interval, current_time, critical, queue, stop_event)
                if error == "timeout":
                    continue  # Kontynuujemy pętlę w przypadku przekroczenia limitu czasu
                elif error:
                    return True  # Zwracamy True, sygnalizując wystąpienie błędu innego niż timeout
            elif task_config and task_config.lower() == "true":
                error = execute_task(task_name, task_func, interval, current_time, critical, queue, stop_event)
                if error == "timeout":
                    continue  # Kontynuujemy pętlę w przypadku przekroczenia limitu czasu
                elif error:
                    return True  # Zwracamy True, sygnalizując wystąpienie błędu innego niż timeout
            elif task_config and task_config.lower() == "false" and critical:
                pass
            else:
                pass

    return False  # Zwracamy False, jeśli nie wystąpił żaden błąd



def execute_task(task_name, task_func, interval, current_time, critical, queue, stop_event):
    if not can_execute_task(task_name, interval, current_time):
        return None  # Nie było błędu, zadanie nie zostało wykonane

    try:
        task_func()
        update_last_execution_time(task_name, current_time)
        time.sleep(2)  # Przerwa tylko jeśli zadanie zostało wykonane
        return None  # Nie było błędu
    except FunctionTimedOut as e:
        queue.put(f"Zadanie {task_name} nie powiodło się: {e}\n")
        cod_restart(queue, stop_event)
        return "timeout"  # Zwracamy specjalną wartość "timeout"
    except Exception as e:
        queue.put(f"Błąd podczas wykonywania zadania {task_name}: {e}\n")
        return e  # Zwracamy obiekt wyjątku
