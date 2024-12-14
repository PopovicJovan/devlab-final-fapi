from sqlalchemy.orm import Session
import app.exceptions as ex
from app.schemas.model import ModelCreate, ModelUpdate
from app.models.model import Model

class ModelView:

    @classmethod
    def model_create(cls, db: Session, modelData: ModelCreate) -> Model:
        try:
            if cls.get_model(db=db, data=modelData):
                raise ex.ModelInUse(detail="Model already exists")
        except ex.ModelNotFound:
            model = Model(**modelData.__dict__)
            db.add(model)
            return model

    @classmethod
    def get_model(cls, db: Session, data: ModelCreate) -> Model:
        model = (db.query(Model)
                 .filter(Model.name == data.name,
                         Model.manufacturer == data.manufacturer)
                 .first())
        if not model:
            raise ex.ModelNotFound
        return model

    @classmethod
    def get_all_model(cls, db: Session) -> list[Model]:
        return db.query(Model).all()


