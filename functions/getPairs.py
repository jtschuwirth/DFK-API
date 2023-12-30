import json

from functions.classes.Pair import Pair

pairsJson = open("data/pairs.json")
pairs_data = json.load(pairsJson)

def getPairs(base_token, chain):
    pairs ={}
    for option in pairs_data:
        if option == base_token:
            for token in pairs_data[base_token]:
                if chain in pairs_data[base_token][token]:
                    pair = Pair(base_token, token, chain)
                    pairs[pair.token]=pair.__dict__
    return pairs
