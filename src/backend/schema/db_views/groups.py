from backend.schema.domain.group_models import GroupMonthly, GroupMonthlyCategory
from backend.schema.domain.value import Value
from backend.schema.db_views import db


class GroupMonthlyDatabase(db.Model):
    __tablename__ = 'group_month'

    month = db.Column(db.String(), primary_key=True)
    account = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    total = db.Column(db.Integer)
    total_out = db.Column(db.Integer)
    total_out_contract = db.Column(db.Integer)
    total_in = db.Column(db.Integer)
    total_in_contract = db.Column(db.Integer)

    def to_domain(self) -> GroupMonthly:
        return GroupMonthly(
            month=self.month, account_acronym=self.account, account_name=self.name, total=Value(self.total),
            total_out=Value(self.total_out), total_out_contract=Value(self.total_out_contract),
            total_in=Value(self.total_in), total_in_contract=Value(self.total_in_contract)
        )


class GroupMonthlyCategoryDatabase(db.Model):
    __tablename__ = 'group_month_category'

    month = db.Column(db.String, primary_key=True)
    account = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String, primary_key=True)
    sum = db.Column(db.Integer)
    acronym = db.Column(db.String)

    def to_domain(self) -> GroupMonthlyCategory:
        return GroupMonthlyCategory(
            month=self.month, account=self.account, name=self.name, category=self.category,
            sum_=Value(self.sum), acronym=self.acronym
        )




