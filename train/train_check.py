# train_check.py

from train.train_utils import read_config

def check_config():
    config_path = "config.json"  # Ścieżka do pliku config.json
    config = read_config(config_path)

    # Sprawdzamy, które comboBoxy są włączone (wartość > 0)
    active_comboboxes = {key: value for key, value in config.items() if value > 0}

    if active_comboboxes:
        print("Active comboBoxes:", active_comboboxes)
        return True
    else:
        print("No active comboBoxes.")
        return False