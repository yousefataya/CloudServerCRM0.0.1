import uuid
from pony.orm import *
from . import MeetingInfo
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class MeetingMember(db.Entity):
    _table_ = ("bank_admin", "meeting_member_info")
    """description of class"""
    memberName = Required(str , column = "member_name")
    memberCode = Required(str , column = "member_code")
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "start_at")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    meetings=Set(MeetingInfo)
    PrimaryKey(id , memberCode)

    @property
    def getMemberName(self):
        return self.memberName + ' ' + self.memberCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.memberName for p in MeetingMember if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByMemberCode(self , memberCode):
        return select(p.memberName for p in MeetingMember if self.memberCode == memberCode)
with db_session:
  # BankInfo who have a Id
  select(p.memberName for p in MeetingMember if  p.findByMemberCode(value))

  # persons who have a car
  select(p.status for p in MeetingMember if  p.status(True))