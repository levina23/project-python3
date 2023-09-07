from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///calendar_app.db'
# Define your database connection
Base = declarative_base()

# Define your models

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    events = relationship("Event", back_populates="user")
    participated_events = relationship("Event", secondary="event_participants", back_populates="participants")

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    color = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    events = relationship("Event", back_populates="category")

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    location = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="events")
    category = relationship("Category", back_populates="events")
    participants = relationship("User", secondary="event_participants", back_populates="participated_events")

event_participants = Table(
    'event_participants',
    Base.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('event_id', Integer, ForeignKey('events.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)


from sqlalchemy import create_engine
DATABASE_URL = 'sqlite:///calendar_app.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
