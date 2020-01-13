import uuid
from pony.orm import *
from . import TeamInfo
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class DepartmentTeam(object):
    _table_ = ("bank_admin", "department_team_info")
    """description of class"""
    departmentName = Required(str , column = "department_name")
    departmentCode = Required(str , column = "department_code" ,  unique=True)
    description = Optional(str , column = "description")
    notes = Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    teams=Set(TeamInfo)
    PrimaryKey(id , teams)


    @property
    def getDepartmentName(self):
        return self.departmentName + ' ' + self.departmentCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.key for p in DepartmentTeam if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByDepartmentName(self , departmentName):
        return select(p.departmentName for p in DepartmentTeam if self.departmentName == departmentName)

with db_session:
  # BankInfo who have a Id
  select(p.departmentName for p in DepartmentTeam if  p.findByDepartmentName(value))

  # persons who have a car
  select(p.status for p in DepartmentTeam if  p.status(True))