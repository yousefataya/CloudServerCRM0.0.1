import uuid
from pony.orm import *
from . import ContractType
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class CustomerContractInfo(db.Entity):
    """description of class"""
    _table_ = ("bank_admin", "customer_contract_info")
    contractName=Required(str , column = "contract_name")
    contractCode=Required(str , column = "contract_code" , unique = True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at_datetime")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    types=Set(ContractType)
    PrimaryKey(id)

    @property
    def getContractName(self):
        return self.contractName + ' ' + self.contractCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.contractName for p in CustomerContractInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByContractCode(self , contractCode):
        return select(p.contractName for p in CustomerContractInfo if self.contractCode == contractCode)
with db_session:
  # BankInfo who have a Id
  select(p.contractName for p in CustomerContractInfo if  p.findByContractCode(value))

  # persons who have a car
  select(p.status for p in CustomerContractInfo if  p.status(True))