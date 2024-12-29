from datetime import datetime

from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

import app.database.database
from app.models.rent import Rent
from app.models import Yacht
from app.views.yacht import YachtView
from app.views.status import StatusView
from app.models.sale import Sale
from app.database.database import database


class StatusCommand:

    @classmethod
    def command(cls):
        db = next(app.database.database.get_db())
        yachts = YachtView.get_all_yacht(db)
        for yacht in yachts:
            if yacht.status_id == StatusView.get_status(db, "unavailable").id: continue
            if cls.yacht_is_sold(db, yacht):
                yacht.status_id = StatusView.get_status(db, "sold").id
            elif cls.yacht_is_rented(db, yacht):
                yacht.status_id = StatusView.get_status(db, "rented").id
            else:
                if (yacht.status_id in
                        [StatusView.get_status(db, "available for rent").id,
                         StatusView.get_status(db, "available for sale").id]):
                    continue
                yacht.status_id = StatusView.get_status(db, "available for rent and sale").id
            db.commit()

    @classmethod
    def yacht_is_sold(cls, db: Session, yacht: Yacht) -> bool:
        return db.query(Sale).filter(Sale.yacht_id == yacht.id).first()

    @classmethod
    def yacht_is_rented(cls, db: Session, yacht: Yacht) -> bool:
        current_time = datetime.now().date()

        return bool(db.execute(
            select(Rent).where(
                Rent.yacht_id == yacht.id,
                Rent.start_date <= current_time,
                Rent.end_date >= current_time
            )
        ).scalars().first())


if __name__ == "__main__":
    StatusCommand.command()

