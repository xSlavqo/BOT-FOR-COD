# test_train.py

from train.train import Train, check_train_end_time

# Tworzymy obiekt Train dla testu
train_vest = Train(name="vest")

# Wywołujemy funkcję testowo
result = check_train_end_time(train_vest)

# Sprawdzamy wynik
print(f"Result for 'vest': {result}")
  