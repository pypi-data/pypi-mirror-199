from colorama import Fore, Back, Style
import random
from builtins import print as pyPrint
import atexit

def print(*args):
    colors = [
        Fore.BLACK,
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.WHITE,
        Fore.RESET,
        Fore.LIGHTBLACK_EX,
        Fore.LIGHTRED_EX,
        Fore.LIGHTGREEN_EX,
        Fore.LIGHTYELLOW_EX,
        Fore.LIGHTBLUE_EX,
        Fore.LIGHTMAGENTA_EX,
        Fore.LIGHTCYAN_EX,
        Fore.LIGHTWHITE_EX,
    ]

    color = random.choice(colors)
    pyPrint(color, end='')
    pyPrint(*args)

def exit_handler():
    pyPrint(Style.RESET_ALL)

atexit.register(exit_handler)