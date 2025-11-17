from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from sql_schemas.Base import Base


class OrderProduct(Base):
    __tablename__ = "order_products"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
