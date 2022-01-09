from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref

from settings import DATABASE_URI

eng = create_engine(DATABASE_URI)

Base = declarative_base()


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base):
    __tablename__ = "user"

    id = Column(String(32), primary_key=True)
    username = Column(String(80), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    line_id = Column(String(120), unique=True, nullable=False)
    role_id = Column(Integer(), ForeignKey("role.id"), nullable=False)
    role = relationship("Role", backref=backref("users"), lazy=False)


Base.metadata.bind = eng

Session = sessionmaker(bind=eng, expire_on_commit=False)

if __name__ == "__main__":
    session = Session()
    users = session.query(User).all()
    session.close()
    for user in users:
        print(user.id, user.username, user.email, user.line_id, user.role.name)
    session.close()
