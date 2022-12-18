from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from functions.autoplayer_table import autoplayer_table
from functions.pricetracker_table import pricetracker_table
from functions.getAlchemistData import getAlchemistData
from functions.getStoneCarverData import getStoneCarverData
from functions.questcomparison import questComparison

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
        pricetracker = pricetracker_table()
        alchemist = getAlchemistData(pricetracker)
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
        pricetracker = pricetracker_table()
        stone_carver = getStoneCarverData(pricetracker)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get stone_carver data")

    response.status_code = status.HTTP_200_OK
    return {"stone_carver": stone_carver}


@app.get("/dfk/quests")
def get_quests(
    response: Response,
):
    quests={}
    try:
        pricetracker = pricetracker_table()
        quests = questComparison(pricetracker, 30)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get quest data")

    response.status_code = status.HTTP_200_OK
    return {"quests": quests}


lambda_handler = Mangum(app, lifespan="off")
