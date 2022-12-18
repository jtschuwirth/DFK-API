import json

IngredientsJson = open("items_data/Alchemist.json")
Ingredients = json.load(IngredientsJson)

def getAlchemistData(pricetracker):
    alchemist = {}
    for recipe in Ingredients:
        alchemist[recipe] = {
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
        alchemist[recipe]["market_cost"] += float(price)

        for item in Ingredients[recipe]:
            price_response = pricetracker.query(
                KeyConditionExpression = "item_ = :item",
                ExpressionAttributeValues={
                ":item": item,
            })
            price = price_response["Items"][-1]["price_"]

            alchemist[recipe]["ingredients"][item] = {
                "quantity":Ingredients[recipe][item],
                "price": Ingredients[recipe][item]*float(price)
            }

            alchemist[recipe]["fabrication_cost"]+=Ingredients[recipe][item]*float(price)
    return alchemist

