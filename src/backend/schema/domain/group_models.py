from backend.schema.domain.value import Value


class GroupMonthly:
    def __init__(self,
                 month: str, account_acronym: str, account_name,
                 total: Value, total_out: Value, total_out_contract: Value,
                 total_in: Value, total_in_contract: Value):
        self.month = month
        self.account_acronym = account_acronym
        self.account_name = account_name
        self.total = total
        self.total_out = total_out
        self.total_out_contract = total_out_contract
        self.total_in = total_in
        self.total_in_contract = total_in_contract


class GroupMonthlyCategory:
    def __init__(self, month: str, account: str, name: str, category: str, sum_: Value, acronym: str):
        self.month: str = month
        self.account: str = account
        self.name: str = name
        self.category: str = category
        self.sum: Value = sum_
        self.acronym: str = acronym
