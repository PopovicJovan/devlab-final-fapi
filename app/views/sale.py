from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
import app.exceptions as exc
from app.models.yacht import Yacht
from app.models.user import User
from app.models.sale import Sale
from app.views.status import StatusView
from app.views.yacht import YachtView
from app.models import Rent


class SaleView:

    @classmethod
    def get_all_sales(cls, db: Session):
        return db.query(Sale).all()

    @classmethod
    def create_sale(cls, db: Session, user: User, yacht: Yacht):
        if not YachtView.yacht_is_available_now_for_sale(db, yacht):
            raise exc.NotAvailable(detail="Yacht is not available for sale")
        if db.execute(select(Rent)
                    .where(Rent.yacht_id == yacht.id,
                            Rent.end_date > datetime.now())
                      ).scalars().all():
            raise exc.NotAvailable(detail="Yacht is not available for sale now")

        sale = Sale(user_id=user.id, yacht_id=yacht.id)
        yacht.status_id = StatusView.get_status(db, "sold").id
        db.add(sale)
        return sale

    @classmethod
    def get_all_sales_for_user(cls, db: Session, user: User):
        return user.sales