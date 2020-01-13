import uuid
from pony.orm import *
from . import AccountCatogry
from . import AccountType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class AccountInfo(db.Entity):
    _table_ = ("bank_admin", "bank_account_info")
    """description of class"""
    id = Required(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    accountCode=Required(str , column = "account_code" , unique = True)
    description=Optional(str , column = "description")
    status=Required(bool , column = "status")
    accountName = Required(str , column = "account_name")
    accountNumber = Required(str , column = "account_number" , unique = True)
    issueDate = Required(datetime , column = "issue_date")
    cvv=Required(str , column = "cvv")
    issuePlace=Optional(str , column = "issue_place")
    accountSerial=Required(str , column = "account_serial" , unique = True)
    notes=Optional(str , column = "notes")
    issueBy=Required(str , column = "issue_by_name")
    issueById=Required(str , column = "issue_by_id")
    catogries=Set(AccountCatogry)
    types=Set(AccountType)
    PrimaryKey(id)

    @property
    def getAccountCode(self):
        return self.accountCode + ' ' + self.accountNumber

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.accountCode for p in AccountInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByAccountCode(self , accountCode):
        return select(p.accountCode for p in AccountInfo if self.accountCode == accountCode)
with db_session:
  # BankInfo who have a Id
  select(p.accountCode for p in AccountInfo if  p.findByAccountCode(value))

  # persons who have a car
  select(p.status for p in AccountInfo if  p.status(True))
