import uuid
from pony.orm import *
from . import DebitCatogry
from . import DebitCurrencyInfo 
from . import DebitType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class DebitByAccount(db.Entity):
    _table_ = ("bank_admin", "debit_account_info")
    """description of class"""
    id = Required(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    debitCode=Required(str , column = "debit_code" , unique = True)
    debitNumber=Required(str , column = "debit_number" , unique = True)
    debitAmount=Required(int , column = "debit_amount" )
    status=Required(bool , column = "status")
    debitCurrency=Required(str , column = "debit_currency")
    issueDate=Required(datetime , column = "issue_date")
    catogries=Set(DebitCatogry)
    types=Set(DebitType)
    currencies=Set(DebitCurrencyInfo)
    PrimaryKey(id)

    @property
    def getDebitCode(self):
        return self.creditCode + ' ' + self.creditNumber

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.creditCode for p in CreditByAccount if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByCreditCode(self , accountCode):
        return select(p.creditCode for p in CreditByAccount if self.creditCode == creditCode)
with db_session:
  # BankInfo who have a Id
  select(p.creditCode for p in CreditByAccount if  p.findByCreditCode(value))

  # persons who have a car
  select(p.status for p in CreditByAccount if  p.status(True))
