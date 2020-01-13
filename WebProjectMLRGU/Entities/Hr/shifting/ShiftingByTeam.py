import uuid
from pony.orm import *
from . import ShiftingByDepartment
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class ShiftingByTeam(object):
    _table_ = ("bank_admin", "shifting_by_team")
    """description of class"""
    teamName=Required(str , column = "team_name")
    shiftName=Required(str , column = "shift_name")
    shiftCode=Required(str , column = "shift_code" , unique=True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "start_at")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    departments=Set('ShiftingByDepartment')
    PrimaryKey(id)


    @property
    def getShiftName(self):
        return self.shiftName + ' ' + self.shiftCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.shiftName for p in ShiftingByTeam if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByShiftCode(self , shiftCode):
        return select(p.shiftName for p in ShiftingByTeam if self.shiftCode == shiftCode)
with db_session:
  # BankInfo who have a Id
  select(p.key for p in ShiftingByTeam if  p.findByShiftCode(value))

  # persons who have a car
  select(p.status for p in ShiftingByTeam if  p.status(True))