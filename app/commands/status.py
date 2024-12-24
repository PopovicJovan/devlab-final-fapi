from sqlalchemy.orm import Session

from app.models import Yacht
from app.views.yacht import YachtView
from app.views.status import StatusView
from app.models.sale import Sale
from app.database.database import database as db
class StatusCommand:


    @classmethod
    def command(cls):
        yachts = YachtView.get_all_yacht(db)
        for yacht in yachts:
            if yacht.status_id == StatusView.get_status(db, "unavailable").id: continue
            if cls.yacht_is_sold(db, yacht):
                yacht.status_id = StatusView.get_status(db, "sold").id
                db.commit()
            elif cls.yacht_is_rented(db, yacht):
                yacht.status_id = StatusView.get_status(db, "rented").id
                db.commit()
            else:
                if (yacht.status_id in
                        [StatusView.get_status(db, "available for rent").id,
                         StatusView.get_status(db, "available for sell").id]):
                    continue
                yacht.status_id = StatusView.get_status(db, "available for rent and sale").id
                db.commit()

    @classmethod
    def yacht_is_sold(cls, db: Session, yacht: Yacht) -> bool:
        return db.query(Sale).filter(Sale.yacht_id == yacht.id).first()

    @classmethod
    def yacht_is_rented(cls, db: Session, yacht: Yacht) -> bool:
        # return db.query(Rent).filter(Rent.yacht_id == yacht.id).first()
        pass