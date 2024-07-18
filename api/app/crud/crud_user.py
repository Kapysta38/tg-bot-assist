from typing import Any, List, Optional, Type

from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models import User
from ..schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self, model):
        super().__init__(model)

    def get(self, db: Session, id: Any):
        return db.query(self.model).filter(self.model.user_id == id).first()

    def get_filter(
            self, db: Session,
            *,
            tg_id: Optional[int] = None
    ) -> List[Type[User]]:
        query = db.query(self.model)
        if tg_id is not None:
            query = query.filter_by(tg_id=tg_id)
        return query.all()


user = CRUDUser(User)
