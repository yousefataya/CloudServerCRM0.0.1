import uuid
from pony.orm import *
from . import JiraCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin' , password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EmployeeJiraInfo(db.Entity):
    _table_ = ("bank_admin", "employee_jira_info")
    """description of class"""
    jiraName=Required(str , column = "jira_name")
    jiraTitle=Required(str , column = "jira_title")
    description=Optional(str , column = "description")
    notes = Optional(str , column = "notes")
    start_at = Required(datetime , 6 , column = "start_at")
    expire_at = Required(datetime , 6 , column = "start_at")
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column = "status")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    PrimaryKey(id)
    catogries= Set(JiraCatogry)
    @property
    def getJiraName(self):
        return self.jiraName + ' ' + self.jiraTitle

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.status for p in EmployeeJiraInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByJiraName(self , jiraName):
        return select(p.jiraName for p in EmployeeJiraInfo if self.jiraName == jiraName)

with db_session:
  # BankInfo who have a Id
  select(p.jiraName for p in EmployeeJiraInfo if  p.findByJiraName(value))

  # persons who have a car
  select(p.status for p in EmployeeJiraInfo if  p.status(True))

