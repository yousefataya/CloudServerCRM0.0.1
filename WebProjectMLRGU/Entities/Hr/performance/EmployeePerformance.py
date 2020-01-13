import uuid
from pony.orm import *
from . import PerformanceCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EmployeePerformance(db.Entity):
    _table_ = ("bank_admin", "emp_performance_main_info")
    """description of class"""
    performanceName=Required(str , column = "performance_name")
    performanceCode=Required(str , column = "performance_code")
    performanceTitle=Required(str , column = "performance_title")
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    PrimaryKey(id)

    @property
    def getPerformanceName(self):
        return self.performanceName + ' ' + self.performanceTitle

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.performanceName for p in EmployeePerformance if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByPerformanceCode(self , memberCode):
        return select(p.performanceName for p in EmployeePerformance if self.memberCode == memberCode)
with db_session:
  # BankInfo who have a Id
  select(p.performanceName for p in EmployeePerformance if  p.findByPerformanceCode(value))

  # persons who have a car
  select(p.status for p in EmployeePerformance if  p.status(True))
