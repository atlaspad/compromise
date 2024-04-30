import json
from eth_account.signers.local import LocalAccount
from eth_account import Account
from web3.auto import w3
from src.sp import read_single_keypress
from src.menu import menupage_getInput, menu
from src.web3net import testnets
import web3


class CompromiseSettings:
    acct: str = None
    atlasprojectDir: str = None
    poolABI: str = None
    poolManAbi: str = None
    chain: str = None
    net: str = None
    nets: dict[dict[str, str]] = None
    infuraapikey: str = None
    genesispooladdr: str = None
    poolmgraddr: str = None
    poolFuns: list[str] = None
    poolManFuns: list[str] = None
    createdTokens: dict[dict[str, str]] = None
    createdPools: dict[dict[str, str]] = None
    acct_instance: Account = None


def load_settings_from_json(settings: CompromiseSettings, json: dict[str, str]):
    settings.acct = json['acct']
    settings.atlasprojectDir = json['atlasprojectDir']
    settings.poolABI = json['poolABI']
    settings.poolManAbi = json['poolManAbi']
    settings.chain = json['chain']
    settings.net = json['net']
    settings.nets = json['nets']
    settings.infuraapikey = json['infuraapikey']
    settings.genesispooladdr = json['genesispooladdr']
    settings.poolmgraddr = json['poolmgraddr']
    settings.poolFuns = json['poolFuns']
    settings.poolManFuns = json['poolManFuns']
    settings.createdTokens = json['createdTokens']
    settings.createdPools = json['createdPools']
    settings.acct_instance = Account.from_key(settings.acct)

def dump_settings_to_json(settings: CompromiseSettings) -> dict[str, object]:
    js=  {
        'acct': settings.acct,
        'atlasprojectDir': settings.atlasprojectDir, 
        'poolABI': settings.poolABI,
        'poolManAbi': settings.poolManAbi,
        'chain': settings.chain,
        'net': settings.net,
        'nets': settings.nets,
        'infuraapikey': settings.infuraapikey, 
        'genesispooladdr': settings.genesispooladdr,
        'poolmgraddr': settings.poolmgraddr,
        'poolFuns': settings.poolFuns,
        'poolManFuns': settings.poolManFuns,
        'createdTokens': settings.createdTokens,
        'createdPools': settings.createdPools
    }
    with open('settings.json', 'w') as f:
        json.dump(js, f)


def set_netchain(settings: CompromiseSettings):
    if settings.nets is None:
        settings.nets = testnets
    chain_names = list(settings.nets.keys())
    chain_names_menu = {net: lambda net=net: net for net in chain_names}
    chain_names_menu['Custom'] = lambda: menupage_getInput('Enter the chain name').display()
    chain_menu = menu(chain_names_menu, 'Select a Chain')
    settings.chain = chain_menu.display()
    if settings.chain not in chain_names:
        RPC = menupage_getInput('Enter the RPC URL').display()
        settings.net = RPC
        settings.nets[settings.chain] = RPC
    else:
        net_names = list(settings.nets[settings.chain].keys())
        net_names_menu = {net: lambda net=net: net for net in net_names}
        net_names_menu['Custom'] = lambda: menupage_getInput('Enter the net name').display()
        net_menu = menu(net_names_menu, 'Select a Network')
        netname = net_menu.display()
        if netname not in net_names:
            settings.nets[settings.chain][netname] = menupage_getInput('Enter the RPC URL').display()
        elif settings.chain == "ETH":
            settings.infuraapikey = menupage_getInput('Enter the Infura API Key','Infura key').display()
            settings.nets[settings.chain][netname] = f'https://{settings.chain}.infura.io/v3/{settings.infuraapikey}'



def set_acct(settings: CompromiseSettings):
    acct = menupage_getInput('Enter the account private key', "Set account").display()
    settings.acct = acct
    settings.acct_instance = Account.from_key(settings.acct)

def set_ABIs(settings: CompromiseSettings):
    poolFile = menupage_getInput('Enter the pool ABI file name',"Set ABIs").display()
    with open (poolFile, 'r') as f:
        settings.poolABI = f.read()
    poolManFile = menupage_getInput('Enter the pool manager ABI file name',"Set ABIs").display()
    with open (poolManFile, 'r') as f:
        settings.poolManAbi = f.read()
    print('last characters of pool ABI:', settings.poolABI[-10:])
    print('last characters of pool manager ABI:', settings.poolManAbi[-10:])

def set_contract_addresses(settings: CompromiseSettings):
    settings.genesispooladdr = menupage_getInput('Enter the genesis pool contract address').display()
    settings.poolmgraddr = menupage_getInput('Enter the pool manager contract address').display()
    dump_settings_to_json(settings)

def setup_wizard(settings: CompromiseSettings):
    set_netchain(settings)
    try:
        set_acct(settings)
    except:
        pass
    settings.atlasprojectDir = menupage_getInput('Enter the AtlasPad Project Directory',"Setup wizard").display()
    set_ABIs(settings)