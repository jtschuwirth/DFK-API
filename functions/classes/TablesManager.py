import boto3

class TablesManager:
    def __init__(self) -> None:
        self.session = boto3.session.Session(
            region_name = "us-east-1",
        )

        self.accounts = self.session.resource('dynamodb').Table("dfk-autoplayer-accounts")
        self.accounts_dev = self.session.resource('dynamodb').Table("dfk-autoplayer-accounts-dev")

        self.autoplayer = self.session.resource('dynamodb').Table("dfk-autoplayer")
        self.gas = self.session.resource('dynamodb').Table("dfk-autoplayer-gas")
        self.history = self.session.resource('dynamodb').Table("dfk-autoplayer-history")
        self.payouts = self.session.resource('dynamodb').Table("dfk-autoplayer-payouts")
        self.managers = self.session.resource('dynamodb').Table("dfk-autoplayer-managers")

        self.buyer_tracking = self.session.resource('dynamodb').Table("dfk-buyer-tracking")
        self.autoplayer_tracking = self.session.resource('dynamodb').Table("dfk-autoplayer-tracking")
        self.profit_tracker = self.session.resource('dynamodb').Table("dfk-profit-tracker")

        self.trades = self.session.resource('dynamodb').Table("dfk-trading-trades")
        self.active_orders = self.session.resource('dynamodb').Table("dfk-trading-active-orders")


    

