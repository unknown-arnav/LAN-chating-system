from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base

engine = create_engine("mysql+pymysql://root:system@localhost/chatroom")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    usna = Column(String(50), unique=True)
    pas = Column(String(255))
    sec = Column(String(255))


user = User(
    usna="leo",
    pas="hash123",
    sec="key123"
)

session.add(user)
session.commit()

print("Dn")