from typing import List, Type

from sqlalchemy.orm import Session

from app.models import Yacht
from app.schemas.yacht import YachtCreate, YachtUpdate
from app.views.model import ModelView
from app.views.status import StatusView
from app import exceptions as ex


class YachtView:

    @classmethod
    def yacht_create(cls, db: Session, yachtData: YachtCreate) -> Yacht:
        try:
            StatusView.get_status_by_id(db, yachtData.status_id)
            ModelView.get_model_by_id(db, yachtData.model_id)
        except ex.ModelNotFound as e:
            raise e
        yacht = Yacht(**yachtData.__dict__)
        db.add(yacht)
        return yacht

    @classmethod
    def yacht_update(cls, db: Session, id: int, yachtData: YachtUpdate) -> Yacht:
        try: yacht = cls.get_yacht_by_id(db, id)
        except ex.ModelNotFound as e: raise e

        if yachtData.status_id:
            try: StatusView.get_status_by_id(db, yachtData.status_id)
            except ex.ModelNotFound as e: raise e
        if yachtData.model_id:
            try: ModelView.get_model_by_id(db, yachtData.model_id)
            except ex.ModelNotFound as e: raise e

        yachtData = yachtData.model_dump(exclude_none=True)
        for key, value in yachtData.items():
            setattr(yacht, key, value)

        return yacht

    @classmethod
    def get_yacht_by_id(cls, db: Session, id: int) -> Yacht:
        yacht = db.query(Yacht).filter(Yacht.id == id).first()
        if not yacht:
            raise ex.ModelNotFound("Yacht not found")
        return yacht

    @classmethod
    def get_all_yacht(cls, db: Session) -> list[Type[Yacht]]:
        return db.query(Yacht).all()

    @classmethod
    def yacht_delete(cls, db: Session, id: int):
        try:
            yacht = cls.get_yacht_by_id(db, id)
            db.delete(yacht)
        except ex.ModelNotFound as e:
            raise e


