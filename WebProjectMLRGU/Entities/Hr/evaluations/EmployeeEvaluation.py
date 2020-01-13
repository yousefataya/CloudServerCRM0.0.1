import uuid
from pony.orm import *
from . import EvaluationCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EmployeeEvaluation(object):
    _table_ = ("bank_admin", "employee_evaluation_info")
    """description of class"""
    evaluationName = Required(str , column = "evaluation_name")
    evaluationTitle = Required(str , column = "evaluation_title")
    description=Optional(str , column = "description")
    notes=Optional(srt , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "expire_at_datetime")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    tasksSuccess=Required(str , column = "tasks_success")
    tasksFail=Optional(str , column = "tasks_fail")
    projectsName=Optional(str , column = "projects_involved")
    PrimaryKey(id,evaluationName)
    catogries = Set(EvaluationCatogry)
    @property
    def getEvaluationName(self):
        return self.evaluationName + ' ' + self.evaluationTitle

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.status for p in EmployeeEvaluation if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByEvaluationName(self , evaluationName):
        return select(p.evaluationName for p in EmployeeEvaluation if self.evaluationName == evaluationName)

with db_session:
  # BankInfo who have a Id
  select(p.evaluationName for p in EmployeeEvaluation if  p.findByEvaluationName(value))

  # persons who have a car
  select(p.status for p in EmployeeEvaluation if  p.status(True))

