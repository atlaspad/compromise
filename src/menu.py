from time import sleep
from typing import Callable
from src.sp import read_single_keypress, no_refresh
from src.banner import banner
from src.gvar import menu_stack
import os
from multiprocessing import Process


class menu:
    menuitems: dict[str, Callable] = None
    onchoose: Callable = None
    title: str = None
    directoryList: str = None
    
    def __init__(self, menuitems: dict[str, Callable], title: str = None, directoryList: list[str] = None, menuName: str = None, onchoose: Callable = None):
        self.menuitems = menuitems
        self.title = title
        self.directoryList = directoryList
        self.onchoose = onchoose
        if menuName is not None:
            global menu_stack
            menu_stack.append(menuName)

    def display(self):
        global menu_stack
        no_refresh()
        os.system('clear')
        banner()

        print('\n\n')
        if len(menu_stack) > 0:
            print(' > '.join(menu_stack))
            print('\n\n')
        i = 0
        for key in self.menuitems:
            print(f'[{i}]: {key}')
            i += 1
        print('\n\n')
        print('q: Quit | Select an option...')
        inp = input()
        if inp == 'q':
            return
        try:
            retval = None
            retval = self.menuitems[list(self.menuitems.keys())[int(inp)]]()
            if retval is not None:
                if len(menu_stack) > 0:
                    menu_stack.pop()
                return retval
        except Exception as e:
            print('Invalid selection')
            print(e)
            read_single_keypress()
        if self.onchoose is not None:
            if len(menu_stack) > 0:
                menu_stack.pop()
            self.onchoose()
        else:
            self.display()


class menupage_getInput:
    query = ''
    name = None
    def __init__(self, query: str, menuName: str = None):
        self.query = query
        if menuName is not None:
            global menu_stack
            menu_stack.append(menuName)
            self.name = menuName
    def display(self):
        global menu_stack
        os.system('clear')
        banner()
        print('\n\n')
        if len(menu_stack) > 0:
            print(' > '.join(menu_stack))
            print('\n\n')
        print(self.query, end=': ')
        inp = input()
        if len(menu_stack) > 0:
            menu_stack.pop()
        return inp


class menupage_asynctask:
    task = None
    task_inprogress_text = ''
    task_stdout = ''
    subp = None
    subp_finished = False

    def __init__(self, task, task_inprogress_text, menu_name: str = None):
        self.task = task
        self.task_inprogress_text = task_inprogress_text
        if menu_name is not None:
            global menu_stack
            menu_stack.append(menu_name)
            self.name = menu_name

    def start_task(self):
        self.task(self.task_stdout)
        self.subp_finished = True

    def display(self):
        global menu_stack
        os.system('clear')
        banner()
        print("\n\n")
        if len(menu_stack) > 0:
            print(' > '.join(menu_stack))
            print('\n\n')
        if not self.subp_finished:
            print(self.task_inprogress_text)
        if self.subp is None:
            self.subp = Process(target=self.start_task)
            self.subp.start()
        print(self.task_stdout)
        if self.subp_finished:
            print('Task complete. Press any key to continue...')
            read_single_keypress()
            return
        sleep(1)
        self.display()
