import uuid
from pony.orm import *
from . import LoggerType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class ManagementLoggerInfo(db.Entity):
    """description of class"""
    _table_ = ("bank_admin", "management_logger_info")
    loggerText=Required(str , column = "logger_text")
    loggerClazz=Required(str , column = "clazz_name")
    loggerMethod=Required(str , column  = "clazz_method")
    description=Optional(str , column = "description")
    notes = Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    types=Set(LoggerType)
    PrimaryKey(id)

    @property
    def geLoggerText(self):
        return self.loggerText + ' ' + self.loggerClazz

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.loggerText for p in ManagementLoggerInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByLoggerClazz(self , loggerClazz):
        return select(p.loggerText for p in ManagementLoggerInfo if self.loggerClazz == loggerClazz)
with db_session:
  # BankInfo who have a Id
  select(p.loggerText for p in ManagementLoggerInfo if  p.findByLoggerClazz(value))

  # persons who have a car
  select(p.status for p in ManagementLoggerInfo if  p.status(True))
