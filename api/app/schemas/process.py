from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from ..shared.types import StatusProcess


class ProcessBase(BaseModel):
    pass


class ProcessCreate(ProcessBase):
    pid: int
    command: str
    log_filename: str
    status: StatusProcess = StatusProcess.running


class ProcessUpdate(ProcessBase):
    status: StatusProcess


class ProcessInDBBase(ProcessBase):
    id: Optional[int]
    pid: Optional[int]
    command: Optional[str]
    log_filename: Optional[str]
    status: StatusProcess
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
