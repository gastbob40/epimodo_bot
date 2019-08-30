from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Date, Boolean, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database.db")
session = sessionmaker(bind=engine)()
Base = declarative_base()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html
# Base.metadata.create_all(engine)

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)

    author_id = Column(Integer)
    channel_id = Column(Integer)

    def __init__(self, author_id: int, channel_id: int):
        self.author_id = author_id
        self.channel_id = channel_id
