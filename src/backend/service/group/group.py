import backend.repository.group_repository as group_repo
import backend.repository.detail_repositroy as repo
from backend.schema.domain.group_models import GroupMonthlyCategory
from backend.schema.domain.value import Value
from backend.schema.dto.group import GroupMonthlyDTO, GroupDetailDTO, ContractsMiniDTO, GroupCategoryDTO

import pandas as pd

from datetime import datetime
from calendar import monthrange

is_active = {
    '12': [12],
    '11': [12],
    '10': [12, 4],
    '09': [12, 3],
    '08': [12],
    '07': [12, 4],
    '06': [12, 2],
    '05': [12, 3],
    '04': [12, 4],
    '03': [12],
    '02': [12],
    '01': [12, 4, 3, 1],
}


class QueryGroupOfAccounts:
    def __init__(self, accounts: list[str], time: str = "monthly"):
        self.accounts = accounts
        self.time = time


class QueryGroupDetails:
    def __init__(self, accounts: list[str], period: str):
        self.accounts = accounts
        self.period = period


class QueryGroupCategory:
    def __init__(self, accounts: list[str], month: str, expense: bool, group_last: int):
        self.accounts = accounts
        self.month = month
        self.expense = expense
        self.group_last = group_last


def get_detail_of_group(query: QueryGroupDetails) -> GroupDetailDTO:
    accounts = query.accounts
    print(accounts)

    contracts = repo.get_all_detailed_contracts()
    pd_contract = pd.DataFrame.from_records([c.get_dict() for c in contracts])
    pd_contract['started_at'] = pd.to_datetime(pd_contract['started_at'])
    pd_contract['finished_at'] = pd.to_datetime(pd_contract['finished_at'])
    pd_contract = pd_contract.query('account_acronym == @accounts')

    transactions = repo.get_all_detailed_transactions()
    pd_transactions = pd.DataFrame.from_records([c.get_dict() for c in transactions])
    pd_transactions['valute'] = pd.to_datetime(pd_transactions['valute'])
    pd_transactions = pd_transactions.query('account_acronym == @accounts')

    year, month = query.period.split('/')
    _, lasts_day = monthrange(year=int(year), month=int(month))
    refference_date_upper = datetime(int(year), int(month), lasts_day)
    refference_date_lower = datetime(int(year), int(month), 1)

    pd_contract_active = pd_contract[pd_contract.started_at <= refference_date_lower]
    pd_contract_active = pd_contract_active[pd_contract_active.finished_at >= refference_date_lower]
    should_in = is_active[month]
    pd_contract_active = pd_contract_active.query('expected_intervall == @should_in')

    pd_transactions_contract = pd_transactions.dropna()
    pd_transactions_contract = pd_transactions_contract[pd_transactions_contract.valute >= refference_date_lower]
    pd_transactions_contract = pd_transactions_contract[pd_transactions_contract.valute <= refference_date_upper]

    full = pd.merge(pd_transactions_contract, pd_contract_active, how='outer', on='contract_id')
    full = full[['valute', 'value', 'expected_value', 'contract_name_y']]

    pd_transactions_non_contracts = pd_transactions[~pd_transactions['contract_id'].notna()]
    pd_transactions_non_contracts = pd_transactions_non_contracts[
        pd_transactions_non_contracts.valute >= refference_date_lower
        ]
    pd_transactions_non_contracts = pd_transactions_non_contracts[
        pd_transactions_non_contracts.valute <= refference_date_upper
        ]

    income_contract = full[full.value > 0].value.sum()
    income_contract_expected = full[full.expected_value > 0].expected_value.sum()

    out_contract = full[full.value < 0].value.sum()
    out_contract_expected = full[full.expected_value < 0].expected_value.sum()

    out = pd_transactions_non_contracts[pd_transactions_non_contracts.value < 0].value.sum() + out_contract
    in_ = pd_transactions_non_contracts[pd_transactions_non_contracts.value > 0].value.sum() + income_contract

    bilanz = in_ + out
    print(f"{bilanz=}, {in_=}, {income_contract_expected=}")
    procent = (float(bilanz) / float(in_) * 100) \
        if float(in_) != 0.0 \
        else (float(bilanz) / float(income_contract_expected) * 100)

    contracts = []
    for contract in full[['contract_name_y', 'value', 'expected_value']].to_numpy():
        contracts.append(
            ContractsMiniDTO(
                name=contract[0],
                expected=Value(contract[2]).get_formatted(),
                value=Value(contract[1]).get_formatted()),
        )

    return GroupDetailDTO(
        income_total=Value(income_contract_expected + in_ - income_contract), income_got=Value(in_),
        income_contract_total=Value(income_contract_expected), income_contract_got=Value(income_contract),
        expense_total=Value(out_contract_expected + out - out_contract),
        expense_got=Value(out), expense_contract_total=Value(out_contract_expected),
        expense_contract_got=Value(out_contract), balance=Value(bilanz), balance_percent=procent, contracts=contracts,
        expected_balance=Value(0), expected_balance_percent=0
    )


def get_group_of_accounts(request: QueryGroupOfAccounts) -> list[GroupMonthlyDTO]:
    accounts = request.accounts
    time = request.time

    groups = group_repo.get_groups_monthly(accounts=accounts, monthly=time)
    groups.reverse()
    dtos: list[GroupMonthlyDTO] = []
    total = 0
    for g in groups:
        month, year = g.month.split("-")
        total = total + g.total.value
        dtos.append(
            GroupMonthlyDTO(
                name=f"{month}/{year}",
                income=g.total_in.get_formatted(),
                outcome=g.total_out.get_formatted(),
                total=g.total.get_formatted(),
                value=Value(total).get_formatted(),
                income_contract=g.total_in_contract.get_formatted(),
                outcome_contract=g.total_out_contract.get_formatted(),
                start="",
                end=""
            )
        )

    dtos.reverse()
    return dtos


def get_group_category(request: QueryGroupCategory) -> list[GroupCategoryDTO]:
    categories: list[GroupMonthlyCategory] = group_repo.get_group_monthly_category(
        accounts=request.accounts,
        month=request.month,
        is_positive=request.expense
    )

    if len(categories) <= request.group_last:
        return [GroupCategoryDTO(
            label=x.category,
            value=float(x.sum.get_decimal()),
            value_formatted=x.sum.get_formatted())
            for x in categories]

    res = [GroupCategoryDTO(
        label=x.category,
        value=float(x.sum.get_decimal()),
        value_formatted=x.sum.get_formatted())
        for x in categories[:request.group_last]]

    val = Value(sum(map(lambda x: x.sum.value, categories[request.group_last+1:])))
    other = GroupCategoryDTO(
        label='Other',
        value=float(val.get_decimal()),
        value_formatted=val.get_formatted()
    )
    res.append(other)

    return res
