from backend.schema.db_views.groups import GroupMonthlyDatabase, GroupMonthlyCategoryDatabase
from backend.schema.domain.group_models import GroupMonthly, GroupMonthlyCategory
from backend.schema.domain.value import Value
from collections import defaultdict


def get_groups_monthly(accounts: list[str], monthly: str) -> list[GroupMonthly]:
    groups: list[GroupMonthlyDatabase] = GroupMonthlyDatabase.query.filter(
        GroupMonthlyDatabase.account.in_(accounts)).all()

    groups_merged = defaultdict(list)
    for obj in groups:
        groups_merged[obj.month].append(obj)

    groups_domain = []
    for g in groups_merged.values():
        groups_domain.append(
            GroupMonthly(
                month=g[0].month,
                account_acronym=g[0].account,
                account_name=g[0].name,
                total=Value(sum([x.total or 0 for x in g])),
                total_out=Value(sum([x.total_out or 0 for x in g])),
                total_out_contract=Value(sum([x.total_out_contract or 0 for x in g])),
                total_in=Value(sum([x.total_in or 0 for x in g])),
                total_in_contract=Value(sum([x.total_in_contract or 0 for x in g])),
            )

        )

    return groups_domain


def get_group_monthly_category(accounts: list[str], month: str, is_positive: bool) -> list[GroupMonthlyCategory]:
    group: list[GroupMonthlyCategoryDatabase] = GroupMonthlyCategoryDatabase.query.filter(
        GroupMonthlyCategoryDatabase.acronym.in_(accounts),
        GroupMonthlyCategoryDatabase.month.like(month),
        (GroupMonthlyCategoryDatabase.sum > 0) if is_positive else (GroupMonthlyCategoryDatabase.sum < 0)
    ).order_by(
        (GroupMonthlyCategoryDatabase.sum.desc()) if is_positive else (GroupMonthlyCategoryDatabase.sum.asc())
    ).all()

    return [x.to_domain() for x in group]

