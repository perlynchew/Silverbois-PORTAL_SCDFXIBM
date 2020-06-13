from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:password@postgres')
base = declarative_base()

class Scdf(base):
    __tablename__ = 'scdf'
    event_id = Column(String, primary_key=True)
    event = Column(String)
    description = Column(String)
    location = Column(String)
    cfr = Column(String)
    status = Column(String)
    date_done = Column(String)
    result = Column(String)

base.metadata.reflect(engine)

Session = sessionmaker(engine)
session = Session()
