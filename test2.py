import re
import pyautogui
import time
from datetime import datetime, timedelta
from tools.functions import save_data, open_data, load_config
from tasks.location import *
from tools.locate import *
from tools.text import *


locate_and_click("pngs/queue_upgrade.png", 0.99, 2)