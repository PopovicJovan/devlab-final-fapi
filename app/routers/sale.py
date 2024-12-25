from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from app.database.database import database
from app.schemas.sale import Sale as SaleSchema
from app.views.sale import SaleView
from app import exceptions as exc
from typing import List, Annotated
from app.views.user import UserView
from app.views.yacht import YachtView

router = APIRouter(prefix="/sale", tags=["sale"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("", response_model=SaleSchema)
def sale_create(db: database, yacht_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        user = UserView.get_user_by_token(db, token)
        yacht = YachtView.get_yacht_by_id(db, yacht_id)
        sale = SaleView.create_sale(db, user, yacht)

        db.commit()
        db.refresh(sale)

        return sale
    except (exc.TokenExpired, exc.InvalidToken, exc.ModelNotFound) as e:
        raise e


@router.get("/my-sales", response_model=List[SaleSchema])
def get_all_sales_for_user(db: database, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        user = UserView.get_user_by_token(db, token)
        return SaleView.get_all_sales_for_user(db, user)
    except (exc.TokenExpired, exc.InvalidToken) as e:
        raise e
