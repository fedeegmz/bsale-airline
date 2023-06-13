from models import AccountData
from serializers import accounts_serializer

def group_accounts(data: list):
    accounts_data: list[AccountData] = [AccountData(**accounts_serializer(account)) for account in data]
    
    accounts_to_update: list[AccountData] = []
    accounts_ready: list[AccountData] = []
    for account in accounts_data:
        if account.seatId == None:
            accounts_to_update.append(account)
        else:
            accounts_ready.append(account)

    return (accounts_to_update, accounts_ready)