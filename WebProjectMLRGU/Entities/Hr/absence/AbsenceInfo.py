import uuid
from pony.orm import *
from . import AbsenceCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class AbsenceInfo(db.Entity):
     _table_ = ("bank_admin", "absence_info")
     """description of class"""
     id = Required(uuid.UUID, default=uuid.uuid4)  
     created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
     PrimaryKey(id)
     catogry=Set(AbsenceCatogry)
     absenceName=Required(str)
     absenceTitle=Required(str)
     absenceDescription=Required(str)
     expiredRecord=Required(bool)
     docs=Optional(bytes)
     deductedDays=Required(int)
     allDays=Required(int)
     status=Required(bool)

@property
def ByAbsenceName(self):
        return self.absenceName + ' ' + self.absenceTitle

@property
@db_session(serializable=True)
def status(self , status):
        select(p.absenceName for p in AbsenceInfo if  self.status == status)

@property
@db_session(serializable=True)
def findByAbsenceName(self , absenceName):
        return select(p.absenceName for p in AbsenceInfo if self.absenceName == bankName)