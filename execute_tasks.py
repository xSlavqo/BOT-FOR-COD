import time
from func_timeout import func_timeout, FunctionTimedOut
from tasks.rss_map import rss_map
from tasks.alliance import ally_help, ally_gifts
from tasks.hospital import hospital
from tasks.train import train_units
from tasks.windows_management import cod_run, cod_restart, tv_close
from tools.functions import load_settings, load_config
from test3 import auto_build

last_execution_time = {}

def execute_task(task_name, task_func, timeout, interval, critical, queue, stop_event):
    current_time = time.time()

    if current_time - last_execution_time.get(task_name, 0) < interval:
        return None

    try:
        if timeout:
            func_timeout(timeout, task_func)
        else:
            task_func()
        
        last_execution_time[task_name] = current_time
        time.sleep(2)
    except FunctionTimedOut:
        queue.put(f"Zadanie {task_name} nie powiodło się: Timeout\n")
        cod_restart(queue, stop_event)
        return "timeout"
    except Exception as e:
        queue.put(f"Błąd podczas wykonywania zadania {task_name}: {e}\n")
        return "general_error"

    return None


def execute_tasks(queue, stop_event):
    config = load_settings()
    reboot_time = load_config().get('reboot_time', 5)

    tasks = [
        ("tv_close", tv_close, 100, 0, True),
        ("cod", cod_run, 100, 0, True),
        ("rss_map", rss_map, 120, 0, False),
        ("hospital", hospital, 30, 1800, False),
        ("train_units", train_units, 200, 0, False),
        ("auto_build", auto_build, 200, 0, True),
        ("ally_help", ally_help, 10, 0, False),
        ("ally_gifts", ally_gifts, 1000, 1800, False),
    ]

    for task_name, task_func, timeout, interval, critical in tasks:
        if config.get(task_name, "").lower() == "true" or (config.get(task_name) is None and critical):
            error = execute_task(task_name, task_func, timeout, interval, critical, queue, stop_event)
            if error:
                if error == "timeout":
                    queue.put("Wystąpił błąd typu 'timeout'. Restartowanie...\n")
                elif error == "general_error":
                    queue.put("Wystąpił błąd typu 'general_error'. Zatrzymanie pętli.\n")
                    return error

                while reboot_time > 0 and not stop_event.is_set():
                    queue.put(f"Restart po błędzie za {reboot_time} sekund\n")
                    time.sleep(1)
                    reboot_time -= 1
                return error

    return False
