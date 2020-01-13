import uuid
from pony.orm import *
from . import CurrencySympole
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class CurrencyInfo(object):
    """description of class"""
    _table_ = ("bank_admin", "currency_info")
    currencyName=Required(str , column = "currency_name")
    currencyCode=Required(str , column = "currency_code" , unique = True)
    description=Optional(str  , column = "description")
    notes=Optional(str , column = "notes")
    expire_at = Required(datetime , 6 , column = "start_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    symboles=Set(CurrencySympole)
    PrimaryKey(id)

    @property
    def getCurrencyName(self):
        return self.currencyName + ' ' + self.currencyCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.currencyName for p in CashInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByCurrencyCode(self , currencyCode):
        return select(p.currencyName for p in CashInfo if self.currencyCode == currencyCode)
with db_session:
  # BankInfo who have a Id
  select(p.currencyName for p in CashInfo if  p.findByCurrencyCode(value))

  # persons who have a car
  select(p.status for p in CashInfo if  p.status(True))