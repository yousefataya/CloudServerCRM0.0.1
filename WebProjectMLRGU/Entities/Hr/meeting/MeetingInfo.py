import uuid
from pony.orm import *
from . import MeetingCatogry
from . import MeetingMember
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class MeetingInfo(db.Entity):
    _table_ = ("bank_admin", "meeting_main_info")
    """description of class"""
    meetingName=Required(str , column = "meeting_name")
    meetingCode=Required(str , column = "meeting_code" , unique=True)
    description=Optional(str , column = "description")
    notes = Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    catogries=Set(MeetingCatogry)
    members=Set('MeetingMember')
    PrimaryKey(id)

    @property
    def geMeetingName(self):
        return self.meetingName + ' ' + self.meetingCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.meetingName for p in MeetingInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByMeetingCode(self , meetingCode):
        return select(p.meetingName for p in MeetingInfo if self.meetingCode == meetingCode)

with db_session:
  # BankInfo who have a Id
  select(p.meetingName for p in MeetingInfo if  p.findByMeetingCode(value))

  # persons who have a car
  select(p.status for p in MeetingInfo if  p.status(True))

