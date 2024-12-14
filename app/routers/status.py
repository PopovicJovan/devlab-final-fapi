from fastapi import APIRouter
from app.database.database import database
from app.schemas.status import StatusCreateUpdate
from app.views.status import StatusView
from app.schemas.status import Status as StatusSchema
from app import exceptions as ex
from typing import List

router = APIRouter(prefix="/status", tags=["status"])


@router.post("", response_model=StatusSchema)
def status_create(db: database, statusData: StatusCreateUpdate):
    # names = ["rented", "sold",
    #           "available for rent",
    #           "available for sell",
    #           "available for rent and sale",
    #           "unavailable"]
    # for name in names:
    #     statusData = StatusCreateUpdate(name=name)
    #     status = StatusView.create_status(db, statusData)
    #     db.commit()
    #     db.refresh(status)
    try:
        status = StatusView.create_status(db, statusData)
        db.commit()
        db.refresh(status)
        return status
    except ex.ModelInUse as e:
        raise e


@router.get("", response_model=List[StatusSchema])
def get_all_status(db: database):
    return StatusView.get_all_status(db)
