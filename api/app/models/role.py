from sqlalchemy import Column, Integer, DateTime, func, Enum
from sqlalchemy.orm import relationship

from ..db.database import Base
from ..shared.types import Roles


class Role(Base):
    __tablename__ = 'user_roles'

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(Enum(Roles), nullable=False)

    user_roles = relationship("UserRole", back_populates="role")
