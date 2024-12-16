from fastapi import APIRouter, UploadFile
from fastapi.params import Depends

from app.database.database import database
from app.schemas.yacht import Yacht, YachtCreate, YachtUpdate
from app import exceptions as ex
from app.views.yacht import YachtView
from typing import List
from app.routers import user as user_router

router = APIRouter(prefix="/yacht", tags=["yacht"])


@router.post("", response_model=Yacht, dependencies=[Depends(user_router.is_admin)])
def yacht_create(db: database, yachtData: YachtCreate):
    try:
        yacht = YachtView.yacht_create(db, yachtData)
        db.commit()
        db.refresh(yacht)
        return yacht
    except ex.ModelNotFound as e:
        raise e


@router.put("/{id}", response_model=Yacht, dependencies=[Depends(user_router.is_admin)])
def yacht_update(id: int, db: database, yachtData: YachtUpdate):
    try:
        yacht = YachtView.yacht_update(db, id, yachtData)
        db.commit()
        db.refresh(yacht)
        return yacht
    except ex.ModelNotFound as e:
        raise e


@router.delete("/{id}", response_model=None, dependencies=[Depends(user_router.is_admin)], status_code=204)
def yacht_delete(id: int, db: database):
    try:
        yacht = YachtView.yacht_delete(db, id)
        db.commit()
        return None
    except ex.ModelNotFound as e:
        raise e

@router.get("", response_model=List[Yacht])
def get_all_yacht(db: database):
    return YachtView.get_all_yacht(db)

@router.get("/{id}", response_model=Yacht)
def get_yacht(id: int, db: database):
    try:
        yacht = YachtView.get_yacht_by_id(db, id)
        return yacht
    except ex.ModelNotFound as e:
        raise e



