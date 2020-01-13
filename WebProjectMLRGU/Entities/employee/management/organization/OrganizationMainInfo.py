import uuid
from pony.orm import *
from . import OrganizationType
from . import OrganizationIndustry
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class OrganizationMainInfo(db.Entity):
    _table_ = ("bank_admin", "organization_main_info")
    """description of class"""
    organizationName=Required(str , column = "organization_name")
    organizationCode=Required(str , column = "organization_code" , unique= True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    types=Set(OrganizationType)
    industries=Set(OrganizationIndustry)
    PrimaryKey(id)

    @property
    def getOrganizationName(self):
        return self.organizationName + ' ' + self.organizationCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.organizationName for p in OrganizationMainInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByOrganizationCode(self , organizationCode):
        return select(p.organizationName for p in OrganizationMainInfo if self.organizationCode == organizationCode)
with db_session:
  # BankInfo who have a Id
  select(p.organizationName for p in OrganizationMainInfo if  p.findByOrganizationCode(value))

  # persons who have a car
  select(p.status for p in OrganizationMainInfo if  p.status(True))