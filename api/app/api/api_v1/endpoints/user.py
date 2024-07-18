from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import models, schemas, crud
from ... import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.UserInDBBase])
def get_users(
        db: Session = Depends(deps.get_db),
        tg_id: Optional[int] = None,
) -> list[models.User]:
    """
    Get all users.
    """
    return crud.user.get_filter(db, tg_id=tg_id)


@router.get("/{id_user}", response_model=schemas.UserInDBBase)
def get_user(
        db: Session = Depends(deps.get_db),
        *,
        id_user: int
) -> models.User:
    """
    Get once user.
    """
    user = crud.user.get(db=db, id=id_user)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.post("/", response_model=schemas.UserInDBBase)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate
) -> models.User:
    """
    Create new user.
    """
    user = crud.user.create(db=db, obj_in=user_in)
    return user


@router.put("/{id_user}", response_model=schemas.UserInDBBase)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        id_user: int,
        user_in: schemas.UserUpdate
) -> Any:
    """
    Update an user.
    """
    user = crud.user.get(db=db, id=id_user)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    upd_user = crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return upd_user
