import json

IngredientsJson = open("items_data/StoneCarver.json")
Ingredients = json.load(IngredientsJson)

def getStoneCarverData(pricetracker):
    stone_carver = {}
    for recipe in Ingredients:
        stone_carver[recipe] = {
            "fabrication_cost": 0,
            "market_cost": 0,
            "ingredients":{}
        }
        price_response = pricetracker.query(
                KeyConditionExpression = "item_ = :item",
                ExpressionAttributeValues={
                ":item": recipe,
            })
        price = price_response["Items"][-1]["price_"]
        stone_carver[recipe]["market_cost"] += float(price)

        for item in Ingredients[recipe]:
            price_response = pricetracker.query(
                KeyConditionExpression = "item_ = :item",
                ExpressionAttributeValues={
                ":item": item,
            })
            price = price_response["Items"][-1]["price_"]

            stone_carver[recipe]["ingredients"][item] = {
                "quantity":Ingredients[recipe][item],
                "price": Ingredients[recipe][item]*float(price)
            }

            stone_carver[recipe]["fabrication_cost"]+=Ingredients[recipe][item]*float(price)
    return stone_carver

