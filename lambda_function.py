from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from functions.ddb_tables import init_tracking_table
from functions.getAlchemistData import getAlchemistData
from functions.getStoneCarverData import getStoneCarverData
from functions.getHeroesByAddress import getHeroes

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
        #table = init_pricetracker_table()
        #alchemist = getAlchemistData(table)
        pass
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
        #table = init_pricetracker_table()
        #stone_carver = getStoneCarverData(table)
        pass
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get stone_carver data")

    response.status_code = status.HTTP_200_OK
    return {"stone_carver": stone_carver}

@app.get("/dfk/buyer/heroes_bought")
def get_heroes_bought(
    response: Response,
):
    heroes_bought = []
    try:
        table = init_tracking_table()
        heroes_bought = table.scan()["Items"]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get heroes bought")

    response.status_code = status.HTTP_200_OK
    return {"heroes": heroes_bought}


lambda_handler = Mangum(app, lifespan="off")
