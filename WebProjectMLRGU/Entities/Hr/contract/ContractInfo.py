import uuid
from pony.orm import *
from . import  ContractCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class ContractInfo(db.Entity):
    _table_ = ("bank_admin", "contract_main_info")
    """description of class"""
    id = Required(uuid.UUID, default=uuid.uuid4)
    contractName=Required(str , column = "contract_name")
    contractTitle=Required(str , column = "contract_title")
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    docs=Required(bytes , column = "docs")
    positionNmae=Required(str , column = "position_name")
    roleName=Required(str , column = "role_name")
    responsibile=Required(str , column = "resposibile_value")
    PrimaryKey(id)
    catgries= Set(ContractCatogry)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "start_at")

@property
def getContractName(self):
        return self.contractName + ' ' + self.contractTitle

@property
@db_session(serializable=True)
def status(self , status):
        select(p.status for p in ContractInfo if  self.status == status)

@property
@db_session(serializable=True)
def findByContractName(self , contractName):
        return select(p.contractName for p in ContractInfo if self.contractName == contractName)

with db_session:
  # BankInfo who have a Id
  select(p.contractName for p in ContractInfo if  p.findByContractName(value))

  # persons who have a car
  select(p.status for p in ContractInfo if  p.status(True))