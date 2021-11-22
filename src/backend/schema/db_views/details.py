import backend.schema.domain.base as m
from backend.schema.domain.value import Value
from backend.schema.db_views import db


class DetailedAccountDatabase(db.Model):
    __tablename__ = 'accounts'
    bank_name = db.Column(db.String())
    bank_acronym = db.Column(db.String())
    account_name = db.Column(db.String())
    id = db.Column(db.String(), primary_key=True)
    acronym = db.Column(db.String())
    number = db.Column(db.String())
    count = db.Column(db.Integer)
    sum = db.Column(db.Integer)

    def to_domain(self):
        return m.Account(
            bank_name=self.bank_name, bank_acronym=self.bank_acronym, account_name=self.account_name,
            account_acronym=self.acronym, account_id=self.id, account_number=self.number, num_transactions=self.count,
            value=self.sum
        )


class DetailedContractDatabase(db.Model):
    __tablename__ = 'contracts'

    avg = db.Column(db.Integer())
    account_acronym = db.Column(db.String())
    account_name = db.Column(db.String())
    count = db.Column(db.Integer())
    contract_id = db.Column(db.String(), primary_key=True)
    contract_namme = db.Column(db.String())
    expected_intervall = db.Column(db.Integer())
    expected_value = db.Column(db.Integer())
    finished_at = db.Column(db.Date())
    interval = db.Column(db.String())
    started_at = db.Column(db.Date())
    sum = db.Column(db.Integer())

    def to_domain(self):
        return m.Contract(
            sum_=Value(self.sum), started_at=self.started_at, intervall=self.interval, finished_at=self.finished_at,
            expected_value=Value(self.expected_value), expected_intervall=self.expected_intervall, count=self.count,
            contract_name=self.contract_namme, contract_id=self.contract_id, avg=Value(self.avg),
            account_name=self.account_name, account_acronym=self.account_acronym
        )


class DetailedTransactionDatabase(db.Model):
    __tablename__ = 'transactions'

    bank_name = db.Column(db.String())
    bank_id = db.Column(db.String())
    account_name = db.Column(db.String())
    account_id = db.Column(db.String())
    account_acronym = db.Column(db.String())
    id_ = db.Column('id', db.String(), primary_key=True)
    issuer = db.Column(db.String())
    valute = db.Column(db.Date())
    value = db.Column(db.Integer())
    category = db.Column(db.String())
    contract_name = db.Column(db.String())
    contract_id = db.Column(db.String())

    def to_domain(self):
        return m.Transaction(
            bank_name=self.bank_name, bank_id=self.bank_id, account_name=self.account_name, account_id=self.account_id,
            account_acronym=self.account_acronym, id_=self.id_, issuer=self.issuer, valute=self.valute,
            value=Value(self.value), category=self.category, contract_name=self.contract_name,
            contract_id=self.contract_id
        )