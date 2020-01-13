import uuid
from pony.orm import *
from . import  ExperincesCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EmployeeExperinces(db.Entity):
    _table_ = ("bank_admin", "employee_experinces_info")
    """description of class"""
    experinceName=Required(str , column = "experince_name")
    experinceTitle=Required(str , column = "experince_title")
    description=Optional(str , column = "description")
    notes = Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    skills=Optional(str , column = "skills")
    id = Required(uuid.UUID, default=uuid.uuid4)
    PrimaryKey(id , experinceName)


    @property
    def getExperinceName(self):
        return self.experinceName + ' ' + self.experinceTitle

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.status for p in EmployeeExperinces if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByExperinceName(self , experinceName):
        return select(p.experinceName for p in EmployeeExperinces if self.experinceName == experinceName)

with db_session:
  # BankInfo who have a Id
  select(p.experinceName for p in EmployeeExperinces if  p.findByExperinceName(value))

  # persons who have a car
  select(p.status for p in EmployeeExperinces if  p.status(True))