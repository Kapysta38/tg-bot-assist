from typing import Any, List, Optional, Type

from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models import Role
from ..schemas import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def __init__(self, model):
        super().__init__(model)

    def get(self, db: Session, id: Any):
        return db.query(self.model).filter(self.model.role_id == id).first()

    def get_filter(
            self, db: Session,
            *,
            role_name: Optional[str] = None
    ) -> List[Type[Role]]:
        query = db.query(self.model)
        if role_name is not None:
            query = query.filter_by(role_name=role_name)
        query = query.all()
        return query


role = CRUDRole(Role)
