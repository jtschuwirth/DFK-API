from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from functions.autoplayer_table import autoplayer_table
from functions.pricetracker_table import pricetracker_table
from functions.addRewardsFromHash import addRewardsFromHash
from functions.getAlchemistData import getAlchemistData 
from functions.getStoneCarverData import getStoneCarverData

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dfk/loot")
def get_loot(
    response: Response, 
    user: str = None,
    start:int = 0,
    end:int =  10**14
    ):
    try:
        if not user: raise Exception("Invalid user")
        user_loot = {
            "address": user,
            "fishing":{},
            "mining":{},
            "total_value":0,
            "total_value_mining":0,
            "total_value_fishing":0,
            "total_txs":0,
            "mining_txs":0,
            "fishing_txs":0
        }
        autoplayer = autoplayer_table()
        pricetracker = pricetracker_table()

        tx_response = autoplayer.query(
            KeyConditionExpression = "address_ = :address AND date_ BETWEEN :startdate AND :enddate",
            ExpressionAttributeValues={
            ":address": user,
            ":startdate": int(start),
            ":enddate": int(end),
        })

        for entry in tx_response["Items"]:
            addRewardsFromHash(entry["hash_"], user_loot, entry["profession_"], pricetracker)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get user loot")

    response.status_code=status.HTTP_200_OK
    return {"loot": user_loot}

@app.get("/dfk/alchemist")
def get_alchemist(
    response: Response, 
    ):
    alchemist = {}
    try:
        pricetracker = pricetracker_table()
        alchemist = getAlchemistData(pricetracker)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get alchemist data")

    response.status_code=status.HTTP_200_OK
    return {"alchemist": alchemist}

@app.get("/dfk/stone_carver")
def get_stone_carver(
    response: Response, 
    ):
    stone_carver = {}
    try:
        pricetracker = pricetracker_table()
        stone_carver = getStoneCarverData(pricetracker)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get stone_carver data")

    response.status_code=status.HTTP_200_OK
    return {"stone_carver": stone_carver}



lambda_handler = Mangum(app, lifespan="off")