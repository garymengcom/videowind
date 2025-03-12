from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, DateTime, JSON, UniqueConstraint


from src.db.connection import Base, create_tables
from src.utils.date_utils import get_now


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=get_now)
    updated_at = Column(DateTime, default=get_now, onupdate=get_now)


class Task(BaseModel):
    __tablename__ = "tasks"

    status = Column(Enum("pending", "processing", "completed", "failed"), default="pending")
    progress = Column(Integer, default=0)
    params = Column(JSON, default={})
    result = Column(JSON, default={})


class Clip(BaseModel):
    __tablename__ = "clips"

    source_name = Column(String(30), nullable=False, default="")
    source_id = Column(String(50), nullable=False, default="")

    path = Column(String(255), nullable=False, unique=True, default="")

    url = Column(String(255), nullable=False, default="")
    thumbnail = Column(String(255), nullable=False, default="")
    width = Column(Integer, nullable=False, default=0)
    height = Column(Integer, nullable=False, default=0)
    duration = Column(Integer, nullable=False, default=0)
    description = Column(Text, default="")

    __table_args__ = (UniqueConstraint("source_name", "source_id"),)


class Term(BaseModel):
    __tablename__ = "terms"

    name = Column(String(50), nullable=False, unique=True)


class ClipTerm(BaseModel):
    __tablename__ = "clips_terms"

    clip_id = Column(Integer, ForeignKey("clips.id"),  nullable=False)
    term_id = Column(Integer, ForeignKey("terms.id"), nullable=False)

    __table_args__ = (UniqueConstraint("clip_id", "term_id"),)


if __name__ == '__main__':
    create_tables()
