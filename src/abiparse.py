import json


class ABIparser:
    pABI: str = None
    funs: list[str] = None
    parsedABI: dict[str, object] = {}
    def __init__(self, pABI: str):
        self.pABI = pABI
        self.funs = []
    def parse(self):
        print('parsing ABI')
        print(self.pABI)
        jsonABI = json.loads(self.pABI)
        for indice in range(len(jsonABI)):
            if jsonABI[indice]['type'] == 'function':
                self.parsedABI[jsonABI[indice]['name']] = jsonABI[indice]["inputs"]
    def getFunction(self, funName: str):
        return self.parsedABI[funName]
