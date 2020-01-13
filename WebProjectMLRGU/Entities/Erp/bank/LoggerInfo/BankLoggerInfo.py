import uuid
from pony.orm import *
from . import LoggerType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class BankLoggerInfo(db.Entity):
    _table_ = ("bank_admin", "bank_logger_info")
    """description of class"""
    id = Required(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    loggerCode=Required(str , column = "logger_code" , unique = True)
    loggerText=Required(str , column = "logger_text" , unique = True)
    loggerClazz=Required(int , column = "logger_clazz" )
    status=Required(bool , column = "status")
    types=Set(LoggerType)
    PrimaryKey(id)

    @property
    def getLoggerCode(self):
        return self.creditCode + ' ' + self.creditNumber

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.loggerCode for p in BankLoggerInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByCreditCode(self , loggerCode):
        return select(p.loggerText for p in BankLoggerInfo if self.loggerCode == loggerCode)
with db_session:
  # BankInfo who have a Id
  select(p.loggerText for p in BankLoggerInfo if  p.findByCreditCode(value))

  # persons who have a car
  select(p.status for p in BankLoggerInfo if  p.status(True))
