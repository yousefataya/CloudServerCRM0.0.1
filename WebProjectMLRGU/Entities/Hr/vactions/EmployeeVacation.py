import uuid
from pony.orm import *
from . import VacationCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EmployeeVacation(db.Entity):
    _table_ = ("bank_admin", "employee_vacations")
    """description of class"""
    vacationName=Required(str , column = "vacation_name")
    vacationCode=Required(str , column = "vacation_code" , unique=True)
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    catogries=Set(VacationCatogry)
    PrimaryKey(id)

    @property
    def getVacationName(self):
        return self.vacationName + ' ' + self.vacationCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.vacationName for p in EmployeeVacation if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByVacationCode(self , vacationCode):
        return select(p.vacationName for p in EmployeeVacation if self.vacationCode == vacationCode)

with db_session:
  # BankInfo who have a Id
  select(p.vacationName for p in EmployeeVacation if  p.findByVacationCode(value))

  # persons who have a car
  select(p.status for p in EmployeeVacation if  p.status(True))

