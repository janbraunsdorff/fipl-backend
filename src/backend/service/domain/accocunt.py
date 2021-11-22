import backend.repository.detail_repositroy as repo
from backend.schema.domain.base import Account
from backend.schema.dto.account import AccountDTOSmall


class QueryAccounts:
    def __init__(self, order_by: str):
        self.order_by = order_by


def get_account_list(query: QueryAccounts) -> list[AccountDTOSmall]:
    account: list[Account] = repo.get_all_detailed_accounts(order_by=query.order_by)
    return [AccountDTOSmall(a) for a in account]
