from fastapi import APIRouter
from app.database.database import database
from app.schemas.model import ModelCreate
from app.schemas.model import Model as ModelSchema
from app import exceptions as ex
from app.views.model import ModelView
from typing import List

router = APIRouter(prefix="/model", tags=["model"])


@router.post("", response_model=ModelSchema)
def model_create(db: database, modelData: ModelCreate):
    try:
        # models = [
        #     {"name": "Sunseeker Predator 55 EVO", "manufacturer": "Sunseeker", "length": 17.05, "width": 4.48},
        #     {"name": "Azimut S6", "manufacturer": "Azimut Yachts", "length": 18.00, "width": 4.75},
        #     {"name": "Ferretti 780", "manufacturer": "Ferretti Yachts", "length": 24.01, "width": 5.80},
        #     {"name": "Princess V50", "manufacturer": "Princess Yachts", "length": 15.49, "width": 4.11},
        #     {"name": "Prestige 590", "manufacturer": "Prestige Yachts", "length": 18.70, "width": 4.84},
        #     {"name": "Beneteau Grand Trawler 62", "manufacturer": "Beneteau", "length": 18.95, "width": 5.45},
        #     {"name": "Fairline Targa 45 GT", "manufacturer": "Fairline Yachts", "length": 14.20, "width": 4.32},
        #     {"name": "Galeon 640 Fly", "manufacturer": "Galeon Yachts", "length": 20.80, "width": 5.00},
        #     {"name": "Riva 76 Perseo Super", "manufacturer": "Riva Yachts", "length": 23.25, "width": 5.75},
        #     {"name": "Lagoon 55", "manufacturer": "Lagoon", "length": 16.56, "width": 9.00},
        # ]
        # for model in models:
        #     m = ModelView.model_create(db, ModelCreate(**model))
        #     db.commit()
        #     db.refresh(m)
        model = ModelView.model_create(db, modelData)
        db.commit()
        db.refresh(model)
        return model
    except ex.ModelInUse as e:
        raise e


@router.get("", response_model=List[ModelSchema])
def get_all_models(db: database):
    return ModelView.get_all_model(db)
