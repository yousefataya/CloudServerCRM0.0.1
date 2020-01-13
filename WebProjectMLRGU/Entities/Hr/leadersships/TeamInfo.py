import uuid
from pony.orm import *
from . import TeamCatogry
from . import TeamMembersInfo
from . import DepartmentTeam
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class TeamInfo(db.Entity):
    _table_ = ("bank_admin", "team_main_info")
    """description of class"""
    teamName=Required(str , column = "team_name")
    teamCode=Required(str , column = "team_code" , unique=True)
    description = Optional(str , column = "description")
    notes = Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "start_at")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    resposibilities=Required(str , column= "tasks")
    catogries = Set(TeamCatogry)
    members=Set('TeamMembersInfo')
    departments=Set('DepartmentTeam')
    PrimaryKey(id)

    @property
    def getTeamName(self):
        return self.teamName + ' ' + self.teamCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.status for p in TeamInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByTeamName(self , teamName):
        return select(p.teamName for p in TeamInfo if self.teamName == teamName)

with db_session:
  # BankInfo who have a Id
  select(p.teamName for p in TeamInfo if  p.findByTeamName(value))

  # persons who have a car
  select(p.status for p in TeamInfo if  p.status(True))



