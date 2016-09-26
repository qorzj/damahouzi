from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

db = create_engine('mysql+mysqldb://name:password@ip/table', pool_recycle=3600)
db.echo = False

Session = sessionmaker(bind=db)
session = Session()

class UserInfo(Base):
    __tablename__ = 'tbl_user_info'
    id = Column(Integer, primary_key=True)
    lpn = Column(String(45))
    carModel = Column(String(90))

objs = []

objs.append(UserInfo(lpn=lpn1, carModel=carModel1))
objs.append(UserInfo(lpn=lpn2, carModel=carModel2))

session.bulk_save_objects(objs)
session.commit()
