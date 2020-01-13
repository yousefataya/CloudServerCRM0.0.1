import uuid
from pony.orm import *
from . import SkillCatogry
from . import SkillType
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EmployeeSkillInfo(db.Entity):
    _table_ = ("bank_admin", "employee_skill_info")
    """description of class"""
    skillName=Required(str , column = "skill_name")
    skillCode=Required(str , column = "skill_code")
    description=Optional(str , column = "description")
    notes=Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "start_at")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    catogries = Set(SkillCatogry)
    types = Set(SkillType)
    PrimaryKey(id)

    @property
    def getShiftName(self):
        return self.skillName + ' ' + self.skillCode

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.skillName for p in EmployeeSkillInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findBySkillCode(self , skillCode):
        return select(p.skillName for p in EmployeeSkillInfo if self.skillCode == skillCode)
with db_session:
  # BankInfo who have a Id
  select(p.skillName for p in EmployeeSkillInfo if  p.findBySkillCode(value))

  # persons who have a car
  select(p.status for p in EmployeeSkillInfo if  p.status(True))
