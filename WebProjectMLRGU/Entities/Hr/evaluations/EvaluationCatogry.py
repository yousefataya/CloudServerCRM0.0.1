import uuid
from pony.orm import *
from . import EmployeeEvaluation
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EvaluationCatogry(db.Entity):
    _table_ = ("bank_admin", "employee_evaluation_catogry_lookup")
    """description of class"""
    id = Required(uuid.UUID, default=uuid.uuid4)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    key=Required(str , column = "key_value")
    description=Optional(str , column = "description")
    status=Required(bool , column = "status")
    docs=Set('EmployeeEvaluation')
    PrimaryKey(id,key)

@property
def getKey(self):
        return self.key + ' ' + self.id

@property
@db_session(serializable=True)
def status(self , status):
        select(p.key for p in EvaluationCatogry if  self.status == status)

@property
@db_session(serializable=True)
def findByKeyName(self , key):
        return select(p.key for p in EvaluationCatogry if self.key == key)

with db_session:
  # BankInfo who have a Id
  select(p.key for p in EvaluationCatogry if  p.findByKeyName(value))

  # persons who have a car
  select(p.status for p in EvaluationCatogry if  p.status(True))


