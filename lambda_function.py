from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from functions.getAlchemistData import getAlchemistData
from functions.getStoneCarverData import getStoneCarverData
from functions.getHeroesByAddress import getHeroes
from functions.TablesManager import TablesManager
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get alchemist data")

    response.status_code = status.HTTP_200_OK
    return alchemist


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
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get stone_carver data")

    response.status_code = status.HTTP_200_OK
    return stone_carver

@app.get("/dfk/buyer/heroes_bought")
def get_heroes_bought(
    response: Response,
):
    heroes_bought = []
    try:
        tablesManager = TablesManager()
        table = tablesManager.buyer_tracker

        heroes_bought = table.scan()["Items"]
        heroes_bought.sort(key=lambda x: int(x["time_"]))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get heroes bought")

    response.status_code = status.HTTP_200_OK
    return heroes_bought

@app.get("/dfk/seller/last_payouts")
def get_last_payouts(
    response: Response,
):
    last_payouts = []
    try:
        tablesManager = TablesManager()
        table = tablesManager.payouts

        last_payouts = list(filter(lambda x: int(x["time_delta"]) != 0, table.scan()["Items"]))
        last_payouts.sort(key=lambda x: float(x["amount_"]))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get last payout")

    response.status_code = status.HTTP_200_OK
    return last_payouts

@app.get("/dfk/seller/tracking_data")
def get_tracking_data(
    response: Response,
):
    tracking_data = []
    try:
        tablesManager = TablesManager()
        table = tablesManager.profit_tracking

        tracking_data = table.scan()["Items"]
        tracking_data.sort(key=lambda x: x["time_"])
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get tracking data")

    response.status_code = status.HTTP_200_OK
    return tracking_data

@app.get("/dfk/accounts/{manager_address}")
def get_accounts_from_manager(
    response: Response,
    manager_address: str
):
    accounts = []
    try:
        tablesManager = TablesManager()
        table = tablesManager.accounts

        scan_response = table.scan(
            FilterExpression="pay_to = :pay_to",
            ExpressionAttributeValues={
                ":pay_to": manager_address
            })
        for item in scan_response["Items"]:
            accounts.append({
                "address": item["address_"],
                "manager": item["pay_to"],
                "enabled": item["enabled_manager"]
                })
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get accounts")

    response.status_code = status.HTTP_200_OK
    return accounts

@app.get("/dfk/trader/trades")
def get_trading_trades(
    response: Response,
):
    trades = []
    try:
        tablesManager = TablesManager()
        table = tablesManager.trades

        trades = table.scan()["Items"]
        trades.sort(key=lambda x: x["time_"])
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get trades")

    response.status_code = status.HTTP_200_OK
    return trades


lambda_handler = Mangum(app, lifespan="off")
