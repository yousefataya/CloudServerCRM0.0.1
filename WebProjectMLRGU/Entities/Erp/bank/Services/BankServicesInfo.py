import uuid
from pony.orm import *
from . import ServiceCatogry
from . import ServiceClazz
from . import ServiceType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class BankServicesInfo(db.Entity):
    _table_ = ("bank_admin", "bank_services_info")
    """description of class"""
    id = Required(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    serviceName=Required(str , column = "service_name")
    serviceCode=Required(str , column = "service_code" , unique=True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    issueDate=Required(datetime , column = "issue_date")
    start_at=Required(datetime , column = "start_at_datetime")
    expire_at=Required(datetime , column = "expire_at_datetime")
    renewableService=Required(bool , column = "renewable_service")
    renewableServiceFees=Required(int , column = "renewable_service_fees")
    serviceCost=Required(int , column = "service_cost")
    catogries=Set(ServiceCatogry)
    clazzs=Set(ServiceClazz)
    types=Set(ServiceType)
    PrimaryKey(id)

    @property
    def getAccountCode(self):
        return self.serviceName + ' ' + self.serviceCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.serviceName for p in BankServicesInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByServiceCode(self , serviceCode):
        return select(p.serviceName for p in BankServicesInfo if self.serviceCode == serviceCode)
with db_session:
  # BankInfo who have a Id
  select(p.serviceName for p in BankServicesInfo if  p.findByServiceCode(value))

  # persons who have a car
  select(p.status for p in BankServicesInfo if  p.status(True))


