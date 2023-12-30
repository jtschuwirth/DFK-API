from functions.classes.Token import Token
import json

itemsJson = open("data/items.json")
items = json.load(itemsJson)

def getTokens(chain):
    tokens = {}
    for item in items:
        if chain in items[item]:
            token = Token(item, chain, None)
            tokens[token.name]=token.__dict__
    return tokens
    