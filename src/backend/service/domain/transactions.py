from datetime import date
from calendar import  monthrange

from backend.repository.detail_repositroy import get_detailed_transactions
from backend.schema.dto.account import TransactionDTOSmall


class QueryTransactions:
    def __init__(self, accounts: list[str], positive: bool, period: str):
        self.accounts: list[str] = accounts
        self.positive = positive
        year, month = period.split('/')
        self.start = date(day=1, month=int(month), year=int(year))
        self.end = date(day=monthrange(year=int(year), month=int(month))[1], month=int(month), year=int(year))


def get_transactions_filtered(request: QueryTransactions) -> list[TransactionDTOSmall]:
    transactions = get_detailed_transactions(
        accounts=request.accounts,
        start=request.start,
        end=request.end,
        positive=request.positive
    )
    return [TransactionDTOSmall(x) for x in transactions]