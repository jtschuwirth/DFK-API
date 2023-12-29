import os
import boto3

class TablesManager:
    def __init__(self, prod) -> None:

        session = boto3.session.Session(
            region_name = "us-east-1",
        )

        self.trades = session.resource('dynamodb').Table("dfk-trading-trades")
        self.accounts = session.resource('dynamodb').Table("dfk-autoplayer-accounts")
        self.gas = session.resource('dynamodb').Table("dfk-autoplayer-gas")
        self.history = session.resource('dynamodb').Table("dfk-autoplayer-history")
        self.autoplayer = session.resource('dynamodb').Table("dfk-autoplayer")
        self.buyer_tracker = session.resource('dynamodb').Table("dfk-buyer-tracking")
        self.payouts = session.resource('dynamodb').Table("dfk-autoplayer-payouts")
        self.profit_tracking = session.resource('dynamodb').Table("dfk-autoplayer-tracking")


    

