import backend.schema.db_views.details as schema
import backend.schema.domain.base as m
from datetime import date


def get_all_detailed_transactions() -> list[m.Transaction]:
    return [x.to_domain() for x in schema.DetailedTransactionDatabase.query.all()]


def get_detailed_transactions(accounts: list[str], positive: bool, start: date, end: date) -> list[m.Transaction]:
    transactions = schema.DetailedTransactionDatabase.query.filter(
        schema.DetailedTransactionDatabase.account_acronym.in_(accounts),
        (schema.DetailedTransactionDatabase.value > 0) if positive else (schema.DetailedTransactionDatabase.value < 0),
        schema.DetailedTransactionDatabase.valute >= start,
        schema.DetailedTransactionDatabase.valute <= end,
    )
    return [x.to_domain() for x in transactions]


def get_all_detailed_accounts(**kwargs) -> list[m.Account]:
    return [x.to_domain() for x in schema.DetailedAccountDatabase.query.all()]


def get_all_detailed_contracts(**kwargs) -> list[m.Contract]:
    return [x.to_domain() for x in schema.DetailedContractDatabase.query.all()]

