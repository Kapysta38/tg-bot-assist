from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import models, schemas, crud
from ... import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ProcessInDBBase])
def get_processes(
        db: Session = Depends(deps.get_db),
) -> list[models.Role]:
    """
    Get all processes.
    """
    return crud.process.get_multi(db)


@router.get("/{id_process}", response_model=schemas.ProcessInDBBase)
def get_process(
        db: Session = Depends(deps.get_db),
        *,
        id_process: int
) -> models.Process:
    """
    Get once process.
    """
    process = crud.process.get(db=db, id=id_process)
    if not process:
        raise HTTPException(status_code=404, detail="process not found")
    return process


@router.post("/", response_model=schemas.ProcessInDBBase)
def create_process(
        *,
        db: Session = Depends(deps.get_db),
        process_in: schemas.ProcessCreate
) -> models.Process:
    """
    Create new process.
    """
    process = crud.process.create(db=db, obj_in=process_in)
    return process


@router.put("/{id_process}", response_model=schemas.ProcessInDBBase)
def update_process(
        *,
        db: Session = Depends(deps.get_db),
        id_process: int,
        process_in: schemas.ProcessUpdate
) -> Any:
    """
    Update an process.
    """
    process = crud.process.get(db=db, id=id_process)
    if not process:
        raise HTTPException(status_code=404, detail="process not found")
    upd_process = crud.process.update(db=db, db_obj=process, obj_in=process_in)
    return upd_process


@router.delete("/{id_process}", response_model=schemas.ProcessInDBBase)
def delete_process(
        *,
        db: Session = Depends(deps.get_db),
        id_process: int,
) -> Any:
    process = crud.process.get(db=db, id=id_process)
    if not process:
        raise HTTPException(status_code=404, detail="process not found")
    upd_role = crud.process.remove(db=db, id=id_process)
    return upd_role
