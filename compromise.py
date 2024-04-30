import json
import os
from src.menu import menu, menupage_getInput
from src.sp import read_single_keypress
from src.settings import CompromiseSettings, load_settings_from_json, dump_settings_to_json, setup_wizard, set_netchain, set_acct, set_ABIs, set_contract_addresses
from src.abiparse import ABIparser
from src.web3utils import web3Utils

ABIs : list[ABIparser] = []

def __debug():
    print('last characters of pool ABI:', settings.poolABI[-10:])
    print('last characters of pool manager ABI:', settings.poolManAbi[-10:])
    read_single_keypress()

def setABIsFromSettings(settings: CompromiseSettings):
    global ABIs
    ABIs.append(ABIparser(settings.poolABI))
    ABIs[0].funs = settings.poolFuns
    ABIs.append(ABIparser(settings.poolManAbi))
    ABIs[1].funs = settings.poolManFuns

def setABIs(settings: CompromiseSettings):
    set_ABIs(settings)
    global ABIs
    ABIs.append(ABIparser(settings.poolABI))
    ABIs.append(ABIparser(settings.poolManAbi))
    dump_settings_to_json(settings)

def load_pool_functions(settings: CompromiseSettings):
    global ABIs
    ABIs[0].parse()
    ABIs[0].funs = settings.poolFuns
    ABIs[1].parse()
    ABIs[1].funs = settings.poolManFuns

def _set_pool_functions():
    ss = menupage_getInput('Enter pool functions separated by commas', 'Set pool functions')
    ss_ret = ss.display()
    lss = ss_ret.split(',')
    global ABIs
    ABIs[0].parse()
    ABIs[0].funs = lss
    settings.poolFuns = lss
    dump_settings_to_json(settings)

def _set_pool_manager_functions():
    ss = menupage_getInput('Enter pool manager functions separated by commas', 'Set pool manager functions')
    ss_ret = ss.display()
    lss = ss_ret.split(',')
    global ABIs
    ABIs[1].parse()
    ABIs[1].funs = lss
    settings.poolManFuns = lss
    dump_settings_to_json(settings)

def set_pool_functions(settings: CompromiseSettings):
    global ABIs
    _menu = menu({
        'Set pool functions': _set_pool_functions,
        'Set pool manager functions': _set_pool_manager_functions,
    }, 'Set ABIs', menuName='Set ABIs')
    _menu.display()

def _contractInteract(web3: web3Utils, ABI: ABIparser, isPool: bool = False):
    if web3 is None:
        if settings.genesispooladdr is None or settings.poolmgraddr is None:
            print('contract addresses are not set!')
            return
        web3 = web3Utils(settings.genesispooladdr, settings.poolmgraddr, settings.acct_instance, settings)
    if ABI.funs is None or len(ABI.funs) == 0:
        print('No functions set for this ABI')
        return
    for i in range(len(ABI.funs)):
        print(f'[{i}]: {ABI.funs[i]}')
    print('q: Quit')
    inp = input()
    if inp == 'q':
        return
    try:
        print('Calling function:', ABI.funs[int(inp)])
        if isPool:
            print(web3.call_pool_contract(ABI.funs[int(inp)], ABI))
        else:
            print(web3.call_pool_manager_contract(ABI.funs[int(inp)], ABI))
    except Exception as e:
        print('Invalid selection')
        print(e)
        read_single_keypress()
    _contractInteract(web3, ABI)

def _setcontractaddresses(settings: CompromiseSettings, web3util: web3Utils):
    set_contract_addresses(settings)
    web3util.poolContractAddr = settings.genesispooladdr
    web3util.poolManAddr = settings.poolmgraddr
def contractInteract(web3: web3Utils):
    if web3 is None:
        if settings.genesispooladdr is None or settings.poolmgraddr is None:
            print('contract addresses are not set!')
            print('press any key to continue')
            read_single_keypress()
            return
    mennnnnu = menu({
        'Genesis Pool': lambda: _contractInteract(web3, ABIs[0], True),
        'Pool Manager': lambda: _contractInteract(web3, ABIs[1])
    }, 'Select contract to interact with')
    mennnnnu.display()
    return
if __name__ == '__main__':
    settings = None
    #check if settings.json exists
    if not os.path.exists('settings.json'):
        settings = CompromiseSettings()
        setup_wizard(settings)
        dump_settings_to_json(settings)
    else:
        with open('settings.json', 'r') as f:
            settings = CompromiseSettings()
            load_settings_from_json(settings, json.load(f))
            setABIsFromSettings(settings)
            load_pool_functions(settings)
            
    web3Man: web3Utils = web3Utils(settings.genesispooladdr, settings.poolmgraddr, settings.acct_instance, settings)
    _menu = menu({
        'Set account via PK': lambda: set_acct(settings),
        'Select/Set chain': lambda: set_netchain(settings),
        'Set contract addresses': lambda: _setcontractaddresses(settings,web3Man),
        'Set ABIs': lambda: setABIs(settings),
        'Set pool functions': lambda: set_pool_functions(settings),
        'Interact with contracts': lambda: contractInteract(web3Man),
        'Debug': __debug
    }, 'Main Menu', menuName='Main Menu')
    _menu.display()