import json

contractsJson = open("data/contracts.json")
contracts = json.load(contractsJson)

class Contract:
    def __init__(self, name, chain):
        self.name = name
        self.chain = chain
        self.address = contracts[name][chain]