import uuid
from pony.orm import *
from . import CustomerType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class CustomerInfo(db.Entity):
    """description of class"""
    _table_ = ("bank_admin", "customer_account_info")
    customerName=Required(str , column = "customer_name")
    customerCode=Required(str , column = "customercode" , unique = True)
    customerFirstName=Required(str , column="first_name")
    customerlastName=Required(str , column = "last_name")
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    status=Required(bool , column = "status")
    id = Required(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    types=Set(CustomerType)
    PrimaryKey(id)

    @property
    def getCustomerName(self):
        return self.customerName + ' ' + self.customerCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.customerName for p in CustomerInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByServiceCode(self , customerCode):
        return select(p.customerName for p in CustomerInfo if self.customerCode == customerCode)
with db_session:
  # BankInfo who have a Id
  select(p.customerName for p in CustomerInfo if  p.findByServiceCode(value))

  # persons who have a car
  select(p.status for p in CustomerInfo if  p.status(True))
