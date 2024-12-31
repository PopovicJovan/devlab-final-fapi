from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.params import Depends
from app.database.database import database
from app.schemas.yacht import Yacht, YachtCreate, YachtUpdate, YachtListResponse, YachtFilter
from app import exceptions as ex
from app.views.yacht import YachtView
from app.routers import user as user_router
from fastapi.security import OAuth2PasswordBearer
import app.exceptions as exc


router = APIRouter(prefix="/yacht", tags=["yacht"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("", response_model=Yacht, dependencies=[Depends(user_router.is_admin)])
def yacht_create(db: database, yachtData: YachtCreate):
    try:
        yacht = YachtView.yacht_create(db, yachtData)
        db.commit()
        db.refresh(yacht)
        picture = YachtView.get_yacht_photo(yacht)
        yacht.picture=f"data:image/jpeg;base64,{picture}" if yacht.picture else None
        return yacht
    except ex.ModelNotFound as e:
        raise e


@router.put("/{id}", response_model=Yacht, dependencies=[Depends(user_router.is_admin)])
def yacht_update(id: int, db: database, yachtData: YachtUpdate):
    try:
        yacht = YachtView.yacht_update(db, id, yachtData)
        db.commit()
        db.refresh(yacht)
        picture = YachtView.get_yacht_photo(yacht)
        yacht.picture=f"data:image/jpeg;base64,{picture}" if yacht.picture else None
        return yacht
    except ex.ModelNotFound as e:
        raise e


@router.delete("/{id}", response_model=None, dependencies=[Depends(user_router.is_admin)], status_code=204)
def yacht_delete(id: int, db: database):
    try:
        YachtView.yacht_delete(db, id)
        db.commit()
        return None
    except ex.ModelNotFound as e:
        raise e
import logging

# Postavljanje osnovne konfiguracije logera
logging.basicConfig(
    level=logging.DEBUG,  # Nivo logovanja (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format loga
    handlers=[logging.StreamHandler()]  # Izlaz na terminal
)
@router.get("", response_model=YachtListResponse)
def get_all_yacht(db: database, filters: YachtFilter = Depends()):
    logging.info(filters)
    try:
        page = filters.page
        yachts = YachtView.get_all_yacht(db, filters)
        pag_yachts = yachts[(page-1)*6:page*6]
        total_pages = (len(yachts) // 6) + int(len(yachts) % 6 != 0)
        for yacht in pag_yachts:
            picture = YachtView.get_yacht_photo(yacht)
            yacht.picture=f"data:image/jpeg;base64,{picture}" if yacht.picture else None
        return YachtListResponse(yachts=pag_yachts, total_pages=total_pages, current_page=page)
    except Exception as e:
        # raise HTTPException(status_code=500, detail="Internal server error")
        raise e


@router.get("/{id}", response_model=Yacht)
def get_yacht(id: int, db: database):
    try:
        yacht = YachtView.get_yacht_by_id(db, id)
        picture = YachtView.get_yacht_photo(yacht)
        yacht.picture=f"data:image/jpeg;base64,{picture}" if yacht.picture else None
        return yacht
    except ex.ModelNotFound as e:
        raise e

@router.post("/{id}/upload-image", response_model=None, dependencies=[Depends(user_router.is_admin)])
def yacht_upload_image(id: int, picture: UploadFile, db: database):
    try:
        yacht = YachtView.get_yacht_by_id(db, id)
        YachtView.yacht_upload_photo(db, yacht, picture)
    except (exc.TokenExpired, exc.InvalidToken, exc.ModelNotFound) as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


