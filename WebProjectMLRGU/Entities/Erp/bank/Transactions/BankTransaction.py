import uuid
from pony.orm import *
from . import TransactionType
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class BankTransaction(db.Entity):
    _table_ = ("bank_admin", "bank_transaction_info")
    """description of class"""
    transactionName=Required(str , column = "transaction_name")
    transactionCode=Required(str , column = "transaction_code" , unique=True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    types=Set(TransactionType)
    PrimaryKey(id)

    @property
    def getTimesheetName(self):
        return self.transactionName + ' ' + self.transactionCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.transactionName for p in BankTransaction if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByTransactionCode(self , transactionCode):
        return select(p.transactionName for p in BankTransaction if self.transactionCode == transactionCode)
with db_session:
  # BankInfo who have a Id
  select(p.transactionName for p in BankTransaction if  p.findByTransactionCode(value))

  # persons who have a car
  select(p.status for p in BankTransaction if  p.status(True))


