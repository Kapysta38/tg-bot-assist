from typing import Any, List, Optional, Type

from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models import UserRole
from ..schemas import UserRoleCreate, UserRoleUpdate


class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleUpdate]):
    def __init__(self, model):
        super().__init__(model)

    def get(self, db: Session, id: Any):
        return db.query(self.model).filter(self.model.user_id == id).first()

    def get_filter(
            self, db: Session,
            *,
            user_id: Optional[int] = None,
            role_id: Optional[int] = None
    ) -> List[Type[UserRole]]:
        query = db.query(self.model)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        if role_id is not None:
            query = query.filter_by(role_id=role_id)
        return query.all()


user_role = CRUDUserRole(UserRole)
