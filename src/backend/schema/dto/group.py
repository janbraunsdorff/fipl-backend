import json
from copy import deepcopy
from backend.schema.domain.value import Value


class GroupMonthlyDTO:
    def __init__(self, name: str, income: str, outcome: str, total: str, value: str,
                 income_contract: str, outcome_contract: str, start: str, end: str
                 ):
        self.name = name
        self.income = income
        self.outcome = outcome
        self.total = total
        self.value = value
        self.incomeContract = income_contract
        self.outcomeContract = outcome_contract
        self.start = start
        self.end = end

    def to_json(self):
        return json.dumps(self.__dict__)


class ContractsMiniDTO:
    def __init__(self, name: str, expected: str, value: str):
        self.name = name
        self.expected = expected
        self.value = value

    def to_json(self):
        return json.dumps(self.__dict__)


class GroupDetailDTO:
    def __init__(self, income_total: Value, income_got: Value, income_contract_total: Value, income_contract_got: Value,
                 expense_total: Value, expense_got: Value, expense_contract_total: Value, expense_contract_got: Value,
                 balance: Value, balance_percent: float, contracts: list[ContractsMiniDTO], expected_balance: Value,
                 expected_balance_percent: float):
        self.incomeTotal = income_total.value
        self.incomeGot = income_got.value
        self.incomeContractTotal = income_contract_total.value
        self.incomeContractGot = income_contract_got.value
        self.incomeTotalBeauty = income_total.get_formatted()
        self.incomeGotBeauty = income_got.get_formatted()
        self.incomeContractTotalBeauty = income_contract_total.get_formatted()
        self.incomeContractGotBeauty = income_contract_got.get_formatted()
        
        self.expenseTotal = expense_total.value
        self.expenseGot = expense_got.value
        self.expenseContractTotal = expense_contract_total.value
        self.expenseContractGot = expense_contract_got.value
        self.expenseTotalBeauty = expense_total.get_formatted()
        self.expenseGotBeauty = expense_got.get_formatted()
        self.expenseContractTotalBeauty = expense_contract_total.get_formatted()
        self.expenseContractGotBeauty = expense_contract_got.get_formatted()

        self.balance = balance.get_formatted()
        self.balancePercent = "{:0.2f}%".format(balance_percent)

        self.expectedBalance = expected_balance.get_formatted()
        self.expectedBalancePercent = "{:0.2f}%".format(expected_balance_percent)

        self.contracts = contracts

    def to_json(self):
        contracts = f"[{','.join([c.to_json() for c in self.contracts])}]"
        attr = self.__dict__.copy()
        attr["contracts"] = '###'
        ret = json.dumps(attr)
        ret = ret.replace('"###"', contracts)
        return ret


class GroupCategoryDTO:
    def __init__(self, label: str, value: float, value_formatted: str):
        self.label = label
        self.value = value
        self.value_formatted = value_formatted

    def to_json(self):
        return json.dumps(self.__dict__)

