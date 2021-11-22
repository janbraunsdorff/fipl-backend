from backend.schema.domain.value import Value
from datetime import date


class Account:
    def __init__(
            self, bank_name: str, bank_acronym: str, account_name: str, account_acronym: str,
            account_id: str, account_number: str, num_transactions: int, value: int):
        self.bank_name = bank_name
        self.bank_acronym = bank_acronym
        self.account_name = account_name
        self.account_acronym = account_acronym
        self.account_id = account_id
        self.account_number = account_number
        self.num_transactions = num_transactions
        self.value = Value(value)


class Contract:
    def __init__(self, sum_: Value, started_at: date, intervall: str, finished_at: date, expected_value: Value,
                 expected_intervall: int, count: int, contract_name: str, contract_id: str, avg: Value,
                 account_name: str, account_acronym: str):
        self.sum: Value = sum_
        self.started_at: date = started_at
        self.interval: str = intervall
        self.finished_at: date = finished_at
        self.expected_value: Value = expected_value
        self.expected_intervall: int = expected_intervall
        self.count: int = count
        self.contract_name: str = contract_name
        self.contract_id: str = contract_id
        self.avg: Value = avg
        self.account_name: str = account_name
        self.account_acronym: str = account_acronym

    def get_dict(self):
        dic = self.__dict__.copy()
        dic['sum'] = self.sum.value
        dic['avg'] = self.avg.value
        dic['expected_value'] = self.expected_value.value
        dic['started_at'] = self.started_at.isoformat()
        dic['finished_at'] = self.finished_at.isoformat()

        return dic

class Transaction:
    def __init__(self, bank_name: str, bank_id: str, account_name: str, account_id: str, account_acronym: str, id_: str,
                 issuer: str, valute: date, value: Value, category: str, contract_name: str, contract_id: str):
        self.bank_name: str = bank_name
        self.bank_id: str = bank_id
        self.account_name: str = account_name
        self.account_id: str = account_id
        self.account_acronym: str = account_acronym
        self.id_: str = id_
        self.issuer: str = issuer
        self.valute: date = valute
        self.value: Value = value
        self.category: str = category
        self.contract_name: str = contract_name
        self.contract_id: str = contract_id

    def get_dict(self):
        dic = self.__dict__.copy()
        dic['valute'] = self.valute.isoformat()
        dic['value'] = self.value.value
        return dic