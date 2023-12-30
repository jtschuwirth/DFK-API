import json

from functions.classes.Contract import Contract

contractsJson = open("data/contracts.json")
contracts_data = json.load(contractsJson)

def getContracts(chain):
    contracts = {}
    for contract in contracts_data:
        if chain in contracts_data[contract]:
            contract = Contract(contract, chain)
            contracts[contract.name]=(contract.__dict__)
    return contracts