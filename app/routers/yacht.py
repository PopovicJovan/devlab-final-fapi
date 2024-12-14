from fastapi import APIRouter, UploadFile
from app.database.database import database
from app.schemas.yacht import Yacht, YachtCreate, YachtUpdate
from app import exceptions as ex
from app.views.yacht import YachtView

router = APIRouter(prefix="/yacht", tags=["yacht"])


@router.post("", response_model=Yacht)
def yacht_create(db: database, yachtData: YachtCreate):
    try:
        yacht = YachtView.yacht_create(db, yachtData)
        db.commit()
        db.refresh(yacht)
        return yacht
    except ex.ModelNotFound as e:
        raise e


@router.put("/{id}", response_model=Yacht)
def yacht_update(id: int, db: database, yachtData: YachtUpdate):
    try:
        yacht = YachtView.yacht_update(db, id, yachtData)
        db.commit()
        db.refresh(yacht)
        return yacht
    except ex.ModelNotFound as e:
        raise e

