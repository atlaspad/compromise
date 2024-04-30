import web3
from eth_account import Account
import web3.tools
from web3.auto import w3
import web3.types
from src.abiparse import ABIparser
from src.settings import CompromiseSettings
from src.menu import menupage_getInput


class web3Utils:
    def __init__(self, poolContractAddr, poolManAddr, acct: Account, settings: CompromiseSettings):
        self.poolContractAddr = poolContractAddr
        self.poolManAddr = poolManAddr
        self.acct = acct
        self.settings = settings
        self.web3 = web3.Web3(web3.HTTPProvider(self.settings.net))
        self.poolContract = self.web3.eth.contract(address=self.poolContractAddr, abi=settings.poolABI)
        self.poolManContract = self.web3.eth.contract(address=self.poolManAddr, abi=settings.poolManAbi)
    def call_pool_contract(self, funName: str, parser: ABIparser):
        args = parser.getFunction(funName)
        builtargs = []
        argindex = 0
        requiresSignature = False
        for arg in args:
            if "components" not in arg.keys():
                val = menupage_getInput(f'Enter {arg["name"]}: (type: {arg["type"]})',f'Setting args for {funName}>{arg["name"]}').display()
                builtargs.append(val)
            else:
                builtargs.append([])
                for internalArg in arg["components"]:
                    val = menupage_getInput(f'Enter {internalArg["name"]}: (type: {internalArg["type"]})',f'Setting args for {funName}>').display()
                    builtargs[argindex].append(val)
            argindex += 1
        return self.poolContract.functions[funName](*args).call()
    def retWeb3Type(self, val: str, type: str):
        match type:
            case "address":
                return w3.to_checksum_address(val)
            case "uint256":
                return w3.to_int(text=val)
            case "bool":
                return bool(val)
            case "string":
                return str(val)
            case "bytes32":
                return w3.to_bytes(text=val)
    
    def call_pool_manager_contract(self, funName: str, parser: ABIparser):
        args = parser.getFunction(funName)
        builtargs = []
        argindex = 0
        for arg in args:
            parsed = False
            while not parsed:
                if arg["name"] == "signature":
                    builtargs.append(self.acct.signHash(self.web3.keccak(text=funName)).signature)
                    parsed = True
                    continue
                elif "components" not in arg.keys():
                    val = menupage_getInput(f'Enter {arg["name"]}: (type: {arg["type"]})',f'Setting args for {funName} > {arg["name"]}').display()
                    try:
                        val = self.retWeb3Type(val, arg["type"])
                        parsed = True
                    except:
                        print('Invalid type')
                        continue
                    builtargs.append(val)
                else:
                    builtargs.append([])
                    for internalArg in arg["components"]:
                        val = menupage_getInput(f'Enter {internalArg["name"]}: (type: {internalArg["type"]})',f'Setting args for {funName} > {arg["name"]}').display()
                        try:
                            val = self.retWeb3Type(val, internalArg["type"])
                            builtargs[argindex].append(val)
                            parsed = True
                        except:
                            print('Invalid type')
                            continue
            argindex += 1
        return self.poolManContract.functions[funName](*builtargs).call()
        