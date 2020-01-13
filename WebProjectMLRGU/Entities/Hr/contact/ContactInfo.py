import uuid
from pony.orm import *
from . import  ContactCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class ContactInfo(db.Entity):
    _table_ = ("bankcore", "contact_main_info")
    """description of class"""
    contactName=Optional(str)
    contactEmail=Optional(str)
    contactMobile=Required(str)
    description=Optional(str)
    notes=Optional(str)
    catogries = Set(ContactCatogry)
    status=Required(bool)
    id = Required(uuid.UUID, default=uuid.uuid4)
    PrimaryKey(id,contactMobile)


@property
def getContactMobile(self):
        return self.contactName + ' ' + self.contactMobile

@property
@db_session(serializable=True)
def status(self , status):
        select(p.status for p in ContactInfo if  self.status == status)

@property
@db_session(serializable=True)
def findByContactMobile(self , contactMobile):
        return select(p.contactMobile for p in ContactInfo if self.contactMobile == contactMobile)

with db_session:
  # BankInfo who have a Id
  select(p.contactMobile for p in ContactInfo if  p.findByContactMobile(value))

  # persons who have a car
  select(p.status for p in ContactInfo if  p.status(True))