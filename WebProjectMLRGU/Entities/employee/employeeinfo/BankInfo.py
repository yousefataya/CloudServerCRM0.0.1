import uuid
from pony.orm import *
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
class BankInfo(db.Entity):
    _table_ = ("bankcore", "Bank_Info")
    """Bank Stander General Information"""
    bankName = Required(str)
    bankAddress = Required(str)
    isQH = Required(bool)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    id = Required(uuid.UUID, default=uuid.uuid4)
    bankCode = Required(uuid.UUID, default=uuid.uuid4)
    PrimaryKey(id , bankCode)

    @property
    def full_name(self):
        return self.bankName + ' ' + self.bankAddress

    @property
    @db_session(serializable=True)
    def isQH(self , isHQ):
        select(p.bankName for p in BankInfo if  self.isQH == isQH)

    @property
    @db_session(serializable=True)
    def findByBankName(self , bankName):
        return select(p.bankName for p in BankInfo if self.bankName == bankName)

class BranchInfo(db.Entity):
    _table_ = ("bankcore", "Bank_Branch_Name")
    """Bank Stander General Information"""
    bankName = Required(str)
    bankAddress = Required(str)
    isQH = Required(bool)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    id = Required(uuid.UUID, default=uuid.uuid4)
    bankCode = Required(uuid.UUID, default=uuid.uuid4)


    @property
    def full_name(self):
        return self.bankName + ' ' + self.bankAddress

    @property
    @db_session(serializable=True)
    def isQH(self , isHQ):
        select(p.bankName for p in BankInfo if  self.isQH == isQH)

    @property
    @db_session(serializable=True)
    def findByBankName(self , bankName):
        return select(p.bankName for p in BankInfo if self.bankName == bankName)



with db_session:
  # BankInfo who have a Id
  select(p.bankName for p in BankInfo if  p.findByBankName(value))

  # persons who have a car
  select(p.bankName for p in BankInfo if  p.isQH(true))


