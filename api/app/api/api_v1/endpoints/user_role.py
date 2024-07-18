from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import models, schemas, crud
from ... import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.UserRoleInDBBase])
def get_user_roles(
        db: Session = Depends(deps.get_db),
        user_id: Optional[int] = None,
        role_id: Optional[int] = None,
) -> list[models.UserRole]:
    """
    Get all user_roles.
    """
    return crud.user_role.get_filter(db, user_id=user_id, role_id=role_id)


@router.post("/", response_model=schemas.UserRoleInDBBase)
def create_user_role(
        *,
        db: Session = Depends(deps.get_db),
        user_role_in: schemas.UserRoleCreate
) -> models.UserRole:
    """
    Create new user_role.
    """
    user_role = crud.user_role.create(db=db, obj_in=user_role_in)
    return user_role


@router.delete("/{id_user_role}", response_model=schemas.UserRoleInDBBase)
def delete_user_role(
        *,
        db: Session = Depends(deps.get_db),
        id_user_role: int,
) -> Any:
    user_role = crud.user_role.get(db=db, id=id_user_role)
    if not user_role:
        raise HTTPException(status_code=404, detail="user_role not found")
    upd_user_role = crud.user_role.remove(db=db, id=id_user_role)
    return upd_user_role
