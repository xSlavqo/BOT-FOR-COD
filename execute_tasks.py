import time
from func_timeout import func_timeout, FunctionTimedOut
from tasks.rss_map import rss_map
from tasks.alliance import ally_help, ally_gifts
from tasks.hospital import hospital
from tasks.train import train_units
from tasks.windows_management import cod_run, cod_restart, tv_close
from tools.functions import load_settings, load_config
from tasks.auto_build import auto_build
from building_menager.main import *

last_execution_time = {}

def execute_task(task_name, task_func, timeout, interval, critical, global_queue, variable_manager, variable_queue, stop_event):
    current_time = time.time()

    if current_time - last_execution_time.get(task_name, 0) < interval:
        return None
    print(f"Próba uruchomienia zadania {task_name}")

    try:
        if timeout:
            result = func_timeout(timeout, task_func)
        else:
            result = task_func()

        last_execution_time[task_name] = current_time
        time.sleep(2)
        
        # Przekazanie wyniku do VariableManager (jeśli jest do tego przeznaczony)
        if result is not None:  # Zakładamy, że funkcja może zwrócić wynik
            variable_queue.put(('variable', task_name, result))

    except FunctionTimedOut:
        global_queue.put(f"Zadanie {task_name} nie powiodło się: Timeout\n")
        cod_restart(global_queue, stop_event)
        return "timeout"
    except Exception as e:
        global_queue.put(f"Błąd podczas wykonywania zadania {task_name}: {e}\n")
        return "general_error"

    return None

def execute_tasks(global_queue, variable_manager, variable_queue, stop_event):
    config = load_settings()
    reboot_time = load_config().get('reboot_time', 5)

    tasks = [
        ("tv_close", tv_close, 100, 0, True),
        ("cod", cod_run, 100, 0, True),
        ("building_main", building_main, 100, 0, True),
        ("rss_map", rss_map, 120, 0, False),
        ("hospital", hospital, 30, 7200, False),
        ("train_units", train_units, 200, 0, False),
        ("auto_build", auto_build, 200, 0, False),
        ("ally_help", ally_help, 10, 0, False),
        ("ally_gifts", ally_gifts, 300, 7200, False),
    ]

    while True:  # Pętla główna dla ponawiania zadań
        for task_name, task_func, timeout, interval, critical in tasks:
            if config.get(task_name, "").lower() == "true" or (config.get(task_name) is None and critical):
                error = execute_task(task_name, task_func, timeout, interval, critical, global_queue, variable_manager, variable_queue, stop_event)
                if error:
                    if error == "timeout":
                        global_queue.put("Wystąpił błąd typu 'timeout'. Restartowanie...\n")
                    elif error == "general_error":
                        global_queue.put("Wystąpił błąd typu 'general_error'. Zatrzymanie pętli.\n")
                        return error  # Zatrzymanie pętli, jeśli inny błąd niż timeout

                    # Odliczanie do restartu po timeout
                    while reboot_time > 0 and not stop_event.is_set():
                        global_queue.put(f"Restart po błędzie za {reboot_time} sekund\n")
                        time.sleep(1)
                        reboot_time -= 1

                    if stop_event.is_set():
                        return error  # Wyjście, jeśli stop_event jest ustawiony

                    global_queue.put("Ponowne uruchamianie zadań po timeout...\n")
                    break  # Restart zadań po timeout
        else:
            break  # Jeśli wszystkie zadania zakończą się bez błędów, wyjście z pętli głównej

    return False
