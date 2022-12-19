from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from functions.heroes_table import heroes_table
from functions.pricetracker_table import pricetracker_table
from functions.getAlchemistData import getAlchemistData
from functions.getStoneCarverData import getStoneCarverData
from functions.questComparison import questComparison
from functions.getHeroes import getHeroes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dfk/alchemist")
def get_alchemist(
    response: Response,
):
    alchemist = {}
    try:
        table = pricetracker_table()
        alchemist = getAlchemistData(table)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get alchemist data")

    response.status_code = status.HTTP_200_OK
    return {"alchemist": alchemist}


@app.get("/dfk/stone_carver")
def get_stone_carver(
    response: Response,
):
    stone_carver = {}
    try:
        table = pricetracker_table()
        stone_carver = getStoneCarverData(table)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get stone_carver data")

    response.status_code = status.HTTP_200_OK
    return {"stone_carver": stone_carver}


@app.get("/dfk/quests")
def get_quests(
    response: Response,
    days: int = 30
):
    quests={}
    try:
        table = pricetracker_table()
        quests = questComparison(table, days)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get quest data")

    response.status_code = status.HTTP_200_OK
    return {"quests": quests}

@app.get("/dfk/heroes")
def get_heroes(
    response: Response,
    address: str = ""
):
    heroes=[]
    try:
        table = heroes_table()
        heroes = table.scan(
                FilterExpression= "owner_ = :address",
                ExpressionAttributeValues={
                ":address": address,
            })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get heroes data")

    response.status_code = status.HTTP_200_OK
    return {"heroes": heroes["Items"]}

@app.get("/dfk/stop_questing")
def stop_questing(
    response: Response,
    address: str = "",
    profession: str = ""
):
    heroes=[]
    try:
        table = heroes_table()
        heroes = table.scan(
                FilterExpression= "owner_ = :address AND profession_ = :profession",
                ExpressionAttributeValues={
                ":address": address,
                ":profession": profession
            })
        for hero in heroes["Items"]:
            table.update_item(
                Key={'owner_': address, "heroId_": hero["heroId_"]},
                UpdateExpression = "SET override_ = :override",
                ExpressionAttributeValues={
                    ':override': "Not Questing"
            })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to stop questing")

    response.status_code = status.HTTP_200_OK
    return {f"Stop {profession}"}

@app.get("/dfk/resume_questing")
def resume_questing(
    response: Response,
    address: str = "",
    profession: str = ""
):
    heroes=[]
    try:
        table = heroes_table()
        heroes = table.scan(
                FilterExpression= "owner_ = :address AND profession_ = :profession",
                ExpressionAttributeValues={
                ":address": address,
                ":profession": profession
            })
        for hero in heroes["Items"]:
            table.update_item(
                Key={'owner_': address, "heroId_": hero["heroId_"]},
                UpdateExpression = "REMOVE override_"
            )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to resume questing")

    response.status_code = status.HTTP_200_OK
    return {f"Resume {profession}"}

@app.get("/dfk/update_heroes")
def update_heroes(
    response: Response,
    address: str = "",
):
    try:
        table = heroes_table()
        heroes_in_address = getHeroes(address)
        for hero in heroes_in_address:
            table.put_item(Item={
                "owner_": address,
                "heroId_": int(hero["id"]),
                "profession_": hero["profession"]

            })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to update heroes")

    response.status_code = status.HTTP_200_OK
    return {f"Updated hero list"}

#Add remove hero endpoint

lambda_handler = Mangum(app, lifespan="off")
