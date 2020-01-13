import uuid
from . import AbsenceInfo 
from pony.orm import *
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class AbsenceCatogry(db.Entity):
    _table_ = ("bank_admin", "absence_catogry_lookup")
    """description of class"""
    id = Required(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    key=Required(str)
    description=Optional(str)
    status=Required(bool)
    absences=Set('AbsenceInfo')
    PrimaryKey(id,key)

@property
def getKey(self):
        return self.key + ' ' + self.id

@property
@db_session(serializable=True)
def status(self , status):
        select(p.key for p in AbsenceCatogry if  self.status == status)

@property
@db_session(serializable=True)
def findByKeyName(self , key):
        return select(p.key for p in AbsenceCatogry if self.key == key)
with db_session:
  # BankInfo who have a Id
  select(p.key for p in AbsenceCatogry if  p.findByKeyName(value))

  # persons who have a car
  select(p.status for p in AbsenceCatogry if  p.status(True))