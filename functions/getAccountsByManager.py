from functions.ddb_tables import init_account_table

def get_accounts(manager_account):
    account_table = init_account_table()
    accounts = []
    scan_response = account_table.scan(
            FilterExpression="enabled_manager = :enabled AND pay_to = :pay_to",
            ExpressionAttributeValues={
                ":enabled": True,
                ":pay_to": manager_account
            })
    for item in scan_response["Items"]:
        accounts.append(item["address_"])
    return accounts