from sqlalchemy import Column, Integer, String, DateTime, func, Enum

from ..db.database import Base
from ..shared.types import StatusProcess


class Process(Base):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True, autoincrement=True)

    pid = Column(Integer)
    command = Column(String(255), nullable=False)
    log_filename = Column(String(255), nullable=False)
    status = Column(Enum(StatusProcess), default=StatusProcess.running)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

