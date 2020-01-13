import uuid
from pony.orm import *
from . import LeaveCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EmployeeLeaveInfo(db.Entity):
    _table_ = ("bank_admin", "employee_leave_info")
    """description of class"""
    leaveName=Required(str , column = "leave_name")
    leaveCode=Required(str , column = "leave_code")
    leaveTitle=Required(str , column = "leave_title")
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    catogries=Set(LeaveCatogry)
    Primary(id,leaveCode)

    @property
    def getLeaveName(self):
        return self.leaveName + ' ' + self.leaveCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.leaveName for p in EmployeeLeaveInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByLeaveName(self , leaveName):
        return select(p.leaveName for p in EmployeeLeaveInfo if self.leaveName == leaveName)

with db_session:
  # BankInfo who have a Id
  select(p.leaveName for p in EmployeeLeaveInfo if  p.findByLeaveName(value))

  # persons who have a car
  select(p.status for p in EmployeeLeaveInfo if  p.status(True))
