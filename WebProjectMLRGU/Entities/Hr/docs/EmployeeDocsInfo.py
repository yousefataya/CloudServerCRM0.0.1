import uuid
from pony.orm import *
from . import DocInfoCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class EmployeeDocsInfo(db.Entity):
    _table_ = ("bank_admin", "employee_docs_main_info")
    """description of class"""
    docName=Required(str , column = "doc_name")
    docExtension=Required(str , column = "doc_extension")
    docType=Required(str , column="doc_type")
    description=Optional(str , column="description")
    notes=Optional(str , column="notes")
    catogries = Set(DocInfoCatogry)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    id = Required(uuid.UUID, default=uuid.uuid4)
    status=Required(bool , column="status")
    PrimaryKey(id , docName)
    @property
    def getDocName(self):
        return self.docName + ' ' + self.docExtension

    @property
    @db_session(serializable=True)
    def status(self , status):
        select(p.status for p in EmployeeDocsInfo if  self.status == status)

    @property
    @db_session(serializable=True)
    def findByDocName(self , docName):
        return select(p.docName for p in EmployeeDocsInfo if self.docName == docName)

with db_session:
  # BankInfo who have a Id
  select(p.docName for p in EmployeeDocsInfo if  p.findByDocName(value))

  # persons who have a car
  select(p.status for p in EmployeeDocsInfo if  p.status(True))




