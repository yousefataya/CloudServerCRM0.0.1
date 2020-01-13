import uuid
from pony.orm import *
from . import AppointmentCatogry
db = Database()
db.bind(provider='oracle', user='bank_admin', password='opc@2020', dsn='ORCL')
db.generate_mapping(create_tables=True)
class AppoiontmentInfo(db.Entity):
    _table_ = ("bank_admin", "appointment_info")
    """description of class"""
    id = Required(uuid.UUID, default=uuid.uuid4)  
    appointmentName=Required(str)
    appointmentTitle=Required(str)
    appointmentDescription=Optional(str)
    status=Required(bool)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    start_at = Required(datetime, 6)
    end_at = Required(datetime, 6)
    appointments=Set(AppointmentCatogry)
    PrimaryKey(id)

@property
def appointmentName(self):
        return self.appointmentName + ' ' + self.appointmentTitle

@property
@db_session(serializable=True)
def status(self , status):
        select(p.status for p in AppoiontmentInfo if  self.status == status)

@property
@db_session(serializable=True)
def findByAppointmentName(self , appointmentName):
        return select(p.appointmentName for p in AppoiontmentInfo if self.appointmentName == appointmentName)

with db_session:
  # BankInfo who have a Id
  select(p.appointmentName for p in AppoiontmentInfo if  p.findByAppointmentName(value))

  # persons who have a car
  select(p.status for p in AppoiontmentInfo if  p.status(True))