import uuid
from pony.orm import *
from . import TimesheetCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EmployeeTimeSheet(db.Entity):
    _table_ = ("bank_admin", "employee_timesheet")
    """description of class"""
    timesheetName=Required(str , column = "timesheet_name")
    timesheetCode=Required(str , column = "timesheet_code")
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at_datetime")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    docs=Required(bytes , column = "doc_sheet_time")
    catgries= Set(TimesheetCatogry)
    PrimaryKey(id,timesheetCode)

    @property
    def getTimesheetName(self):
        return self.timesheetName + ' ' + self.timesheetCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.timesheetName for p in EmployeeTimeSheet if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByTimesheetCode(self , timesheetCode):
        return select(p.timesheetName for p in EmployeeTimeSheet if self.timesheetCode == timesheetCode)
with db_session:
  # BankInfo who have a Id
  select(p.timesheetName for p in EmployeeTimeSheet if  p.findByTimesheetCode(value))

  # persons who have a car
  select(p.status for p in EmployeeTimeSheet if  p.status(True))
