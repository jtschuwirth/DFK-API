def price(item, pricetracker):
    value = pricetracker.query(
        KeyConditionExpression="item_ = :item",
        ExpressionAttributeValues={
            ":item": item,
        })
    return float(value["Items"][-1]["price_"])


def questComparison(pricetracker, days):
    quests = {}
    avg_gold_per_mining = 60
    training_success = 0.35
    quests["mining"] = {
        "items": {
            "DFKGold": {
                "amount": avg_gold_per_mining*2.88*days,
                "value":  price("DFKGold", pricetracker)*avg_gold_per_mining*2.88*days
            },
            "Shvas Rune": {
                "amount": 0.015*5*2.88*days,
                "value":  price("Shvas Rune", pricetracker)*0.015*5*2.88*days
            },
            "Gaias Tears": {
                "amount": 0.175*5*2.88*days,
                "value":  price("Gaias Tears", pricetracker)*0.105*5*2.88*days
            }
        }
    }

    quests["vitality"] = {
        "items": {
            "DFKGold": {
                "amount": 25*5*3*training_success*days,
                "value":  price("DFKGold", pricetracker)*25*5*3*training_success*days
            },
            "Shvas Rune": {
                "amount": 0.01*5*3*training_success*days,
                "value":  price("Shvas Rune", pricetracker)*0.01*5*3*training_success*days
            },
            "Lesser Vigor Crystal": {
                "amount": 0.005*5*3*training_success*days,
                "value":  price("Lesser Vigor Crystal", pricetracker)*0.005*5*3*training_success*days
            }
        }
    }

    quests["fishing"] = {
        "items": {
            "Frost Bloater": {
                "amount": 0.23*5*3*days,
                "value":  price("Frost Bloater", pricetracker)*0.23*5*3*days
            },
            "Lanterneye": {
                "amount": 0.09*5*3*days,
                "value":  price("Lanterneye", pricetracker)*0.09*5*3*days
            },
            "Ironscale": {
                "amount": 0.09*5*3*days,
                "value":  price("Ironscale", pricetracker)*0.09*5*3*days
            },
            "Speckle Tail": {
                "amount": 0.06*5*3*days,
                "value":  price("Speckle Tail", pricetracker)*0.06*5*3*days
            },
            "Three-Eyed Eel": {
                "amount": 0.01*5*3*days,
                "value":  price("Three-Eyed Eel", pricetracker)*0.01*5*3*days
            },
            "King Pincer": {
                "amount": 0.01*5*3*days,
                "value":  price("King Pincer", pricetracker)*0.01*5*3*days
            },
            "Shimmerskin": {
                "amount": 0.009*5*3*days,
                "value":  price("Shimmerskin", pricetracker)*0.009*5*3*days
            },
            "Shvas Rune": {
                "amount": 0.01*5*3*days,
                "value":  price("Shvas Rune", pricetracker)*0.01*5*3*days
            },
            "Gaias Tears": {
                "amount": 0.075*5*3*days,
                "value":  price("Gaias Tears", pricetracker)*0.075*5*3*days
            }
        }
    }

    quests["foraging"] = {
        "items": {
            "Frost Drum": {
                "amount": 0.23*5*3*days,
                "value":  price("Frost Drum", pricetracker)*0.23*5*3*days
            },
            "Knaproot": {
                "amount": 0.06*5*3*days,
                "value":  price("Knaproot", pricetracker)*0.09*5*3*days
            },
            "Rockroot": {
                "amount": 0.09*5*3*days,
                "value":  price("Rockroot", pricetracker)*0.09*5*3*days
            },
            "Darkweed": {
                "amount": 0.06*5*3*days,
                "value":  price("Darkweed", pricetracker)*0.06*5*3*days
            },
            "Ambertaffy": {
                "amount": 0.04*5*3*days,
                "value":  price("Ambertaffy", pricetracker)*0.01*5*3*days
            },
            "Skunk Shade": {
                "amount": 0.009*5*3*days,
                "value":  price("Skunk Shade", pricetracker)*0.01*5*3*days
            },
            "Shaggy Caps": {
                "amount": 0.01*5*3*days,
                "value":  price("Shaggy Caps", pricetracker)*0.009*5*3*days
            },
            "Shvas Rune": {
                "amount": 0.01*5*3*days,
                "value":  price("Shvas Rune", pricetracker)*0.01*5*3*days
            },
            "Gaias Tears": {
                "amount": 0.075*5*3*days,
                "value":  price("Gaias Tears", pricetracker)*0.075*5*3*days
            }
        }
    }

    for quest in quests:
        quests[quest]["total_value"] = 0
        for item in quests[quest]["items"]:
            quests[quest]["total_value"] += quests[quest]["items"][item]["value"]
            
    return quests
