from sqlalchemy.orm import Session

from app.models.status import Status
from app.schemas.status import StatusCreateUpdate
from app import exceptions as ex
from typing import List


class StatusView:

    @classmethod
    def create_status(cls, db: Session, statusData: StatusCreateUpdate) -> Status:
        statusData.name = statusData.name.value
        try:
            if cls.get_status(db=db, name=statusData.name):
                raise ex.ModelInUse(detail="Status already exists")
        except ex.ModelNotFound:
            status = Status(**statusData.__dict__)
            db.add(status)
            return status

    @classmethod
    def get_status(cls, db: Session, name: str) -> Status:
        status = db.query(Status).filter(Status.name == name).first()
        if not status:
            raise ex.ModelNotFound(detail="Status not found")
        return status

    @classmethod
    def get_all_status(cls, db: Session) -> List[type[Status]]:
        return db.query(Status).all()
