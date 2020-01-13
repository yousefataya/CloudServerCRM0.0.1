import uuid
from pony.orm import *
from  . import ProductType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class ProductInfo(db.Entity):
    _table_ = ("bank_admin", "product_main_info")
    """description of class"""
    productName=Required(str , column = "product_name")
    productCode=Required(str , column = "product_code" , unique= True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    types=Set(ProductType)
    PrimaryKey(id)

    @property
    def getProductName(self):
        return self.productName + ' ' + self.productCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.productName for p in ProductInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByProductCode(self , productCode):
        return select(p.productName for p in ProductInfo if self.productCode == productCode)
with db_session:
  # BankInfo who have a Id
  select(p.partnerName for p in ProductInfo if  p.findByProductCode(value))

  # persons who have a car
  select(p.status for p in ProductInfo if  p.status(True))
