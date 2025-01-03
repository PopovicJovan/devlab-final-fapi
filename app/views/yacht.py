from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, not_, exists
from app.models import Yacht, Model, Rent
from app.schemas.yacht import YachtCreate, YachtUpdate, YachtFilter
from app.views.model import ModelView
from app.views.status import StatusView
from app import exceptions as ex
from fastapi import UploadFile
import uuid
import shutil
import os
import base64
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
        try:
            yacht = cls.get_yacht_by_id(db, id)
        except ex.ModelNotFound as e:
            raise e

        if yachtData.status_id:
            try:
                StatusView.get_status_by_id(db, yachtData.status_id)
            except ex.ModelNotFound as e:
                raise e
        if yachtData.model_id:
            try:
                ModelView.get_model_by_id(db, yachtData.model_id)
            except ex.ModelNotFound as e:
                raise e

        yachtData = yachtData.model_dump(exclude_none=True)
        for key, value in yachtData.items():
            setattr(yacht, key, value)

        return yacht

    @classmethod
    def get_yacht_by_id(cls, db: Session, id: int) -> Yacht:
        yacht = db.query(Yacht).filter(Yacht.id == id).first()
        if not yacht: raise ex.ModelNotFound("Yacht not found")
        return yacht

    @classmethod
    def get_all_yacht(cls, db: Session, filters: YachtFilter) -> list[Yacht]:
        name = filters.name
        model_id = filters.model_id
        minLength = filters.minLength
        maxLength = filters.maxLength
        minWidth = filters.minWidth
        maxWidth = filters.maxWidth
        minPrice = filters.minPrice
        maxPrice = filters.maxPrice
        sort_by = filters.sort_by.name
        startDate = filters.startDate
        endDate = filters.endDate

        query = db.query(Yacht)
        if name:
            query = query.filter(Yacht.name.ilike(f"%{name}%"))
        if model_id:
            query = query.filter(Yacht.model_id == model_id)
        if minLength:
            query = query.filter(Yacht.model.has(Model.length >= minLength))
        if maxLength:
            query = query.filter(Yacht.model.has(Model.length <= maxLength))
        if minWidth:
            query = query.filter(Yacht.model.has(Model.width >= minWidth))
        if maxWidth:
            query = query.filter(Yacht.model.has(Model.width <= maxWidth))
        if minPrice:
            query = query.filter(Yacht.sale_price >= minPrice)
        if maxPrice:
            query = query.filter(Yacht.sale_price <= maxPrice)
        if startDate and endDate:
            query = query.filter(
                not_(
                    exists().where(
                        and_(
                            Rent.yacht_id == Yacht.id,
                            Rent.start_date <= endDate,
                            Rent.end_date >= startDate
                        )
                    )
                )
            )

        if sort_by:
            if "available_for_rent" == sort_by:
                query = query.filter(or_(Yacht.status_id == StatusView.get_status(db, "available for rent").id,
                                         Yacht.status_id == StatusView.get_status(db,
                                                                                  "available for rent and sale").id))
            if "available_for_sale" == sort_by:
                query = query.filter(or_(Yacht.status_id == StatusView.get_status(db, "available for sale").id,
                                         Yacht.status_id == StatusView.get_status(db,
                                                                                  "available for rent and sale").id))
            if "price_asc" == sort_by:
                query = query.order_by(Yacht.sale_price.asc())
        else:
            query = query.order_by(Yacht.sale_price.desc())
        return query.all()

    @classmethod
    def yacht_delete(cls, db: Session, id: int):
        try:
            yacht = cls.get_yacht_by_id(db, id)
            db.delete(yacht)
        except ex.ModelNotFound as e:
            raise e

    @classmethod
    def yacht_upload_photo(cls, db: Session, yacht: Yacht, picture: UploadFile) -> None:
        if not os.path.exists(os.path.abspath(cls.IMAGE_ROOT)):
            os.makedirs(os.path.abspath(cls.IMAGE_ROOT))

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

    @classmethod
    def yacht_is_available_now_for_rent(cls, db: Session, yacht: Yacht):
        available_statuses = [
            StatusView.get_status(db, "available for rent and sale").id,
            StatusView.get_status(db, "available for rent").id
        ]
        return yacht.status_id in available_statuses

    @classmethod
    def yacht_is_available_now_for_sale(cls, db: Session, yacht: Yacht):
        available_statuses = [
            StatusView.get_status(db, "available for rent and sale").id,
            StatusView.get_status(db, "available for sale").id
        ]
        return yacht.status_id in available_statuses
