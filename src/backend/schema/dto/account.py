from backend.schema.domain.base import Account, Transaction
import json


class AccountDTOSmall:
    def __init__(self, account: Account):
        self.id: str = account.account_acronym
        self.bankName: str = account.bank_name
        self.name: str = account.account_name
        self.balance: str = account.value.get_formatted()
        self.isPositive: bool = account.value.is_positive()

    def to_json(self):
        return json.dumps(self.__dict__)


class TransactionDTOSmall:
    def __init__(self, transaction: Transaction):
        self.issuer = transaction.issuer
        self.category = transaction.category
        self.valute = transaction.valute.isoformat()
        self.value = transaction.value.get_formatted()

    def to_json(self):
        return json.dumps(self.__dict__)