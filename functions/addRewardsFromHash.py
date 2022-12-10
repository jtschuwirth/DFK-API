from functions.provider import w3
from web3.logs import DISCARD
import json 

QuestCoreJson = open("abi/QuestCoreV2.json")
QuestCoreABI = json.load(QuestCoreJson)

ContractsJson = open("items_data/Contracts_dfkchain.json")
Contracts = json.load(ContractsJson)

decimalsJson = open("items_data/decimals.json")
decimals_data = json.load(decimalsJson)

quest_core_contract = w3.eth.contract(address = "0xE9AbfBC143d7cef74b5b793ec5907fa62ca53154", abi = QuestCoreABI)

def addRewardsFromHash(hash, user_loot, profession, pricetracker):
    reward_receipt = w3.eth.get_transaction_receipt(hash)
    quest_reward = quest_core_contract.events.RewardMinted().processReceipt(reward_receipt, errors=DISCARD)

    for reward in quest_reward:
        item = Contracts[reward["args"]["reward"]]
        decimals = 0

        #TODO: add date sorting to get the price when the item was obtained
        price_response = pricetracker.query(
            KeyConditionExpression = "item_ = :item",
            ExpressionAttributeValues={
            ":item": item,
        })
        price = price_response["Items"][0]["price_"]
        if item in decimals_data:
            decimals = decimals_data[item]
        if not item in user_loot[profession]:
            user_loot[profession][item] = {"amount": 0, "price": 0}
        user_loot[profession][item]["amount"] += reward["args"]["amount"]/10**decimals
        user_loot[profession][item]["price"] += (reward["args"]["amount"]/10**decimals)*float(price)
        user_loot["total_value"] += (reward["args"]["amount"]/10**decimals)*float(price)
        if profession == "mining":
            user_loot["total_value_mining"] += (reward["args"]["amount"]/10**decimals)*float(price)
        elif profession == "fishing":
            user_loot["total_value_fishing"] += (reward["args"]["amount"]/10**decimals)*float(price)
    if profession == "mining":
        user_loot["mining_txs"]+=1
    elif profession == "fishing":
        user_loot["fishing_txs"]+=1
    user_loot["total_txs"]+=1