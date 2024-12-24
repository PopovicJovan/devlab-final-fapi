from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.params import Depends

from app.database.database import database, get_db
from app.schemas.yacht import Yacht, YachtCreate, YachtUpdate
from app import exceptions as ex
from app.views.yacht import YachtView
from typing import List
from app.routers import user as user_router
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.views.user import UserView



router = APIRouter(prefix="/yacht", tags=["yacht"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



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
    try:
        yachts = YachtView.get_all_yacht(db)
        return yachts
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{id}", response_model=Yacht)
def get_yacht(id: int, db: database):
    try:
        yacht = YachtView.get_yacht_by_id(db, id)
        return yacht
    except ex.ModelNotFound as e:
        raise e

@router.post("/{id}/upload-image", response_model=str)
def yacht_upload_image(id: int, picture: UploadFile, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
    try:
        current_user = UserView.get_user_by_token(db, token)
        
        YachtView.yacht_upload_photo(db, id,current_user, picture)
        return "Image uploaded successfully"
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


