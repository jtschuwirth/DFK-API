import os
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from functions.classes.TablesManager import TablesManager
from dotenv import load_dotenv
import logging
from functions.getContract import getContracts
from functions.getPairs import getPairs

from functions.getTokens import getTokens

logger = logging.getLogger()
logger.setLevel(logging.INFO)
load_dotenv()

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
        pass
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get stone_carver data")

    response.status_code = status.HTTP_200_OK
    return stone_carver

@app.get("/dfk/buyer/heroes_bought/{profession}")
def get_heroes_bought(
    response: Response,
    profession: str
):
    heroes_bought = []
    try:
        tablesManager = TablesManager(os.environ["PROD"] == "true")
        table = tablesManager.buyer_tracking

        heroes_bought = table.scan(
            FilterExpression="profession = :profession",
            ExpressionAttributeValues={":profession": profession}
            )["Items"]
        heroes_bought.sort(key=lambda x: int(x["time_"]))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get heroes bought")

    response.status_code = status.HTTP_200_OK
    return heroes_bought

@app.get("/dfk/target_accounts/{manager_address}/{profession}")
def get_target_accounts(
    response: Response,
    manager_address: str,
    profession: str
):
    target_accounts = []
    try:
        tablesManager = TablesManager(os.environ["PROD"] == "true")
        table = tablesManager.managers

        if profession == "gardening":
            target_accounts = table.scan(
                FilterExpression="address_ = :address_",
                ExpressionAttributeValues={":address_": manager_address}
                )["Items"][0]["target_accounts_gardening"]
        elif profession == "mining":
            target_accounts = table.scan(
                FilterExpression="address_ = :address_",
                ExpressionAttributeValues={":address_": manager_address}
                )["Items"][0]["target_accounts_mining"]

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get target accounts")

    response.status_code = status.HTTP_200_OK
    return target_accounts

@app.get("/dfk/seller/last_payouts/{manager_address}")
def get_last_payouts(
    response: Response,
    manager_address: str
):
    last_payouts = []
    try:
        tablesManager = TablesManager(os.environ["PROD"] == "true")
        table = tablesManager.payouts

        last_payouts = list(filter(lambda x: int(x["time_delta"]) != 0, table.scan(
            FilterExpression="payout_address = :payout_address",
            ExpressionAttributeValues={
                ":payout_address": manager_address
            })["Items"]))
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
        tablesManager = TablesManager(os.environ["PROD"] == "true")
        table = tablesManager.autoplayer_tracking

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
        tablesManager = TablesManager(os.environ["PROD"] == "true")
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
                "profession": item["profession"] if "profession" in item else "mining",
                "enabled": item["enabled_manager"]
                })
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get accounts")

    response.status_code = status.HTTP_200_OK
    return accounts

@app.get("/dfk/accounts/{manager_address}/{profession}")
def get_accounts_from_manager_by_profession(
    response: Response,
    manager_address: str,
    profession: str
):
    accounts = []
    try:
        tablesManager = TablesManager(os.environ["PROD"] == "true")
        table = tablesManager.accounts

        scan_response = table.scan(
            FilterExpression="pay_to = :pay_to AND profession = :profession",
            ExpressionAttributeValues={
                ":pay_to": manager_address,
                ":profession": profession
            })
        for item in scan_response["Items"]:
            accounts.append(item["address_"])
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
        tablesManager = TablesManager(os.environ["PROD"] == "true")
        table = tablesManager.trades

        trades = table.scan()["Items"]
        trades.sort(key=lambda x: x["time_"])
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get trades")

    response.status_code = status.HTTP_200_OK
    return trades

@app.get("/dfk/tokens")
def get_tokens(
    response: Response,
    chain: str
):
    tokens = {}
    try:
        tokens = getTokens(chain)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get tokens")

    response.status_code = status.HTTP_200_OK
    return tokens

@app.get("/dfk/tokens/trade")
def get_tokens(
    response: Response,
    chain: str
):
    tokens = {}
    try:
        tokens = getTokens(chain, True)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get tokens")

    response.status_code = status.HTTP_200_OK
    return tokens

@app.get("/dfk/pairs")
def get_pairs(
    response: Response,
    token: str,
    chain: str
):
    pairs = {}
    try:
        pairs = getPairs(token, chain)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get pairs")

    response.status_code = status.HTTP_200_OK
    return pairs

@app.get("/dfk/contracts")
def get_contracts(
    response: Response,
    chain: str
):
    contracts = {}
    try:
        contracts = getContracts(chain)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get contracts")

    response.status_code = status.HTTP_200_OK
    return contracts


lambda_handler = Mangum(app, lifespan="off")
