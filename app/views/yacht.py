from typing import List, Type

from sqlalchemy.orm import Session

from app.models import Yacht
from app.schemas.yacht import YachtCreate, YachtUpdate
from app.views.model import ModelView
from app.views.status import StatusView
from app import exceptions as ex
from fastapi import UploadFile
import uuid
import shutil
import os
import base64
from app.models.user import User
from sqlalchemy import select
from typing import Union

class YachtView:
    IMAGE_ROOT = "./app/public/images/yachts"
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
        picture = YachtView.get_yacht_photo(yacht)
        if picture:
            yacht.picture=f"data:image/jpeg;base64,{picture}"
        else:
            yacht.picture=None
        return yacht

    @classmethod
    def get_all_yacht(cls, db: Session) -> list[Yacht]:
        yachts= db.query(Yacht).all()
        for yacht in yachts:
            picture = cls.get_yacht_photo(yacht)
            yacht.picture=f"data:image/jpeg;base64,{picture}" if picture else None
        return yachts


    @classmethod
    def yacht_delete(cls, db: Session, id: int):
        try:
            yacht = cls.get_yacht_by_id(db, id)
            db.delete(yacht)
        except ex.ModelNotFound as e:
            raise e

    @classmethod
    def yacht_upload_photo(cls, db: Session, yacht_id: int, current_user:User, picture: UploadFile) -> None:
        if not current_user.admin:
            raise PermissionError("You are not authorised to use this route!")
        
        if not os.path.exists(os.path.abspath(cls.IMAGE_ROOT)):
            os.makedirs(os.path.abspath(cls.IMAGE_ROOT))

        yacht = db.execute(select(Yacht).where(Yacht.id == yacht_id)).scalar_one_or_none()
        if not yacht:
            raise ValueError("Yacht not found")

        if yacht.picture:
            old_picture = f"{cls.IMAGE_ROOT}/{yacht.picture}"
            if os.path.exists(old_picture):
                os.remove(old_picture)

        unique_filename = f"{uuid.uuid4()}.jpg"
        new_path = f"{cls.IMAGE_ROOT}/{unique_filename}"
        with open(new_path, "wb") as f:
            shutil.copyfileobj(picture.file, f)

        yacht.picture = unique_filename
        db.commit()

    @classmethod
    def get_yacht_photo(cls, yacht: Yacht) -> Union[None, str]:
        if not yacht.picture:
            return None

        image_path = f"{cls.IMAGE_ROOT}/{yacht.picture}"
        with open(image_path, "rb") as image:
            image = image.read()

        return base64.b64encode(image).decode("utf-8")
