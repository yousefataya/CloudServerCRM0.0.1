import uuid
from pony.orm import *
from . import ShiftingByTeam
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class ShiftingByDepartment(db.Entity):
    _table_ = ("bank_admin", "shifting_by_department")
    """description of class"""
    departmentName=Required(str , column = "department_name")
    shiftName=Required(str , column = "shift_name")
    shiftCode=Required(str , column = "shift_code" , unique=True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    teams=Set(ShiftingByTeam)
    PrimaryKey(id)

    @property
    def getShiftName(self):
        return self.shiftName + ' ' + self.shiftCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.shiftName for p in ShiftingByDepartment if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByShiftCode(self , shiftCode):
        return select(p.shiftName for p in ShiftingByDepartment if self.shiftCode == shiftCode)
with db_session:
  # BankInfo who have a Id
  select(p.key for p in ShiftingByDepartment if  p.findByShiftCode(value))

  # persons who have a car
  select(p.status for p in ShiftingByDepartment if  p.status(True))
