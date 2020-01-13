import uuid
from pony.orm import *
from . import CashType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class CashInfo(db.Entity):
    """description of class"""
    _table_ = ("bank_admin", "cash_management_info")
    cashName=Required(str , column = "cash_name")
    cashCode=Required(str , column = "cash_code" , unique=True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at_datetime")
    expire_at = Required(datetime , 6 , column = "start_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    types=Set(CashType)
    PrimaryKey(id)

    @property
    def getCashName(self):
        return self.cashName + ' ' + self.cashCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.cashName for p in CashInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByCashName(self , cashCode):
        return select(p.cashName for p in CashInfo if self.cashCode == cashCode)
with db_session:
  # BankInfo who have a Id
  select(p.cashName for p in CashInfo if  p.findByCashName(value))

  # persons who have a car
  select(p.status for p in CashInfo if  p.status(True))