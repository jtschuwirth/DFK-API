import boto3
from boto3 import Session

class TablesManager:
    def __init__(self, prod) -> None:
        self.session: Session = boto3.session.Session(
            region_name = "us-east-1",
        )

        if prod:
            self.accounts = self.session.resource('dynamodb').Table("dfk-autoplayer-accounts")
        else:
            self.accounts = self.session.resource('dynamodb').Table("dfk-autoplayer-accounts-dev")

        self.autoplayer = self.session.resource('dynamodb').Table("dfk-autoplayer")
        self.gas = self.session.resource('dynamodb').Table("dfk-autoplayer-gas")
        self.history = self.session.resource('dynamodb').Table("dfk-autoplayer-history")
        self.payouts = self.session.resource('dynamodb').Table("dfk-autoplayer-payouts")
        self.fees = self.session.resource('dynamodb').Table("dfk-autoplayer-fee")
        self.managers = self.session.resource('dynamodb').Table("autodfk-managers")

        self.buyer_tracking = self.session.resource('dynamodb').Table("dfk-buyer-tracking")
        self.autoplayer_tracking = self.session.resource('dynamodb').Table("dfk-autoplayer-tracking")
        self.profit_tracker = self.session.resource('dynamodb').Table("dfk-profit-tracker")

        self.trades = self.session.resource('dynamodb').Table("dfk-trading-trades")
        self.active_orders = self.session.resource('dynamodb').Table("dfk-trading-active-orders")

        self.mining_stats = self.session.resource('dynamodb').Table("dfk-autoplayer-mining-stats")
        self.gardening_stats = self.session.resource('dynamodb').Table("dfk-autoplayer-gardening-stats")
        self.fishing_stats = self.session.resource('dynamodb').Table("dfk-autoplayer-fishing-stats")
        self.foraging_stats = self.session.resource('dynamodb').Table("dfk-autoplayer-foraging-stats")


    