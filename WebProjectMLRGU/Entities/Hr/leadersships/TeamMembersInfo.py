import uuid
from pony.orm import *
from . import TeamInfo
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class TeamMembersInfo(db.Entity):
    _table_ = ("bank_admin", "team_members_info")
    """description of class"""
    memberName=Required(str , column = "member_name")
    roleName=Required(str , column = "role_name")
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    teams=Set(TeamInfo)
    PrimaryKey(id , teams)

    @property
    def getMemberName(self):
        return self.memberName + ' ' + self.roleName

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.key for p in TeamMembersInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByMemberName(self , memberName):
        return select(p.memberName for p in TeamMembersInfo if self.memberName == memberName)

with db_session:
  # BankInfo who have a Id
  select(p.memberName for p in TeamMembersInfo if  p.findByMemberName(value))

  # persons who have a car
  select(p.status for p in TeamMembersInfo if  p.status(True))

