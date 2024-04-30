from pyfiglet import Figlet
import random


def banner():
    _banner();

def _banner():
    f = Figlet(font='slant')
    print(f.renderText('Compromise'))
    with open('src/lyrics.txt', 'r') as file:
        lines = file.readlines()
        print(random.choice(lines).strip('\n'), end='...\n')