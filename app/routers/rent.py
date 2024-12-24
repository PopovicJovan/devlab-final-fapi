from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.rent import RentCreate, RentResponse
from app.views.rent import RentView
from app.views.user import UserView

router = APIRouter(prefix="/rents", tags=["Rents"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/", response_model=RentResponse)
def create_rent(rent_data: RentCreate, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
    try:
        current_user= UserView.get_user_by_token(db, token)
        return RentView.create_rent(db, rent_data, current_user)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
        
    
@router.delete("/{rent_id}", response_model=str)
def cancel_rent(rent_id: int, db: Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
    try:
        current_user = UserView.get_user_by_token(db, token)
        return RentView.cancel_rent(db, rent_id, current_user)
    except Exception as e:
        print(f"Error2: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    
