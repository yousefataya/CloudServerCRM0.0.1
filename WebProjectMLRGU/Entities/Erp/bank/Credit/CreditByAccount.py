import uuid
from pony.orm import *
from . import CreditCatogry
from . import CreditType
from . import CreditCurrencyInfo
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class CreditByAccount(db.Entity):
    _table_ = ("bank_admin", "credit_account_info")
    """description of class"""
    id = Required(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    creditCode=Required(str , column = "credit_code" , unique = True)
    creditNumber=Required(str , column = "credit_number" , unique = True)
    creditAmount=Required(int , column = "credit_amount" )
    status=Required(bool , column = "status")
    creditCurrency=Required(str , column = "credit_currency")
    issueDate=Required(datetime , column = "issue_date")
    catogries=Set(CreditCatogry)
    types=Set(CreditType)
    currencies=Set(CreditCurrencyInfo)
    PrimaryKey(id)

    @property
    def getAccountCode(self):
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
