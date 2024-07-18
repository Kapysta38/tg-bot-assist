from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import models, schemas, crud
from ... import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.RoleInDBBase])
def get_roles(
        db: Session = Depends(deps.get_db),
        role_name: Optional[str] = None,
) -> list[models.Role]:
    """
    Get all roles.
    """
    return crud.role.get_filter(db, role_name=role_name)


@router.post("/", response_model=schemas.RoleInDBBase)
def create_role(
        *,
        db: Session = Depends(deps.get_db),
        role_in: schemas.RoleCreate
) -> models.Role:
    """
    Create new role.
    """
    role = crud.role.create(db=db, obj_in=role_in)
    return role


@router.delete("/{id_role}", response_model=schemas.RoleInDBBase)
def delete_role(
        *,
        db: Session = Depends(deps.get_db),
        id_role: int,
) -> Any:
    role = crud.role.get(db=db, id=id_role)
    if not role:
        raise HTTPException(status_code=404, detail="role not found")
    upd_role = crud.role.remove(db=db, id=id_role)
    return upd_role
