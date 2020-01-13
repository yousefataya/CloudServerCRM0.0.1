import uuid
from pony.orm import *
from . import PartnerType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class PartnerInfo(db.Entity):
    _table_ = ("bank_admin", "partner_main_info")
    """description of class"""
    partnerName=Required(str , column = "partner_name")
    partnerCode=Required(str , column = "partner_code" , unique= True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    types=Set(PartnerType)
    PrimaryKey(id)

    @property
    def getPartnerName(self):
        return self.partnerName + ' ' + self.partnerCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.partnerName for p in PartnerInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByPartnerCode(self , partnerCode):
        return select(p.partnerName for p in PartnerInfo if self.partnerCode == partnerCode)
with db_session:
  # BankInfo who have a Id
  select(p.partnerName for p in PartnerInfo if  p.findByPartnerCode(value))

  # persons who have a car
  select(p.status for p in PartnerInfo if  p.status(True))
