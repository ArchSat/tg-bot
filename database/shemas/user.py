import os

from sqlalchemy import create_engine, Column, Integer, JSON
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

host = str(os.getenv("HOST"))
password = str(os.getenv("PASSWORD"))
database = str(os.getenv("DATABASE"))

engine = create_engine(f"sqlite:///database.db")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_settings = Column(JSON)
    pictures_settings = Column(JSON)


Base.metadata.create_all(bind=engine)
