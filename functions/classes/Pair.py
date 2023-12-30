import json

pairsJson = open("data/pairs.json")
pairs_data = json.load(pairsJson)

class Pair:
    def __init__(self, base_token, token, chain):
        self.base_token = base_token
        self.token = token
        self.chain = chain
        self.address = pairs_data[base_token][token][chain]