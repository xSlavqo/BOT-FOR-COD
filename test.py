from tasks.location import *
from tools.locate import *
from tasks.windows_management import *

from tools.find import find_and_click

def autobuild():
    cod_run()
    city()
    while find_and_click("pngs/build.png", 0.999, 3, 0, 60, 5):
        locate_and_click("pngs/build2.png", 0.99, 0, 0, 5)
        locate_and_click("pngs/build3.png", 0.99, 0, 0, 5)
        locate_and_click("pngs/build4.png", 0.99, 0, 0, 5)
        locate_and_click("pngs/build5.png", 0.99, 0, 0, 5)
        while locate_and_click("pngs/ask_help.png", 0.95, 0, 0, 5):
            None
        map()
        city()

autobuild()