from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.schemas.rent import RentCreate, Rent
from app.views.rent import RentView
from app.views.user import UserView
from app.database.database import database
import app.exceptions as exc

router = APIRouter(prefix="/rents", tags=["Rents"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("", response_model=Rent)
def create_rent(rent_data: RentCreate, db: database, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        current_user= UserView.get_user_by_token(db, token)
        rent = RentView.create_rent(db, rent_data, current_user)
        db.commit()
        db.refresh(rent)
        return rent
    except (exc.TokenExpired, exc.InvalidToken, exc.ModelNotFound, exc.NotAvailable) as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.delete("/{rent_id}", response_model=None, status_code=204)
def cancel_rent(rent_id: int, db: database, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        current_user = UserView.get_user_by_token(db, token)
        RentView.cancel_rent(db, rent_id, current_user)
    except (exc.TokenExpired, exc.InvalidToken, exc.ModelNotFound, exc.ForbidenException) as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    
