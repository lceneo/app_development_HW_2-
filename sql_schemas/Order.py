from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID, uuid4

from sql_schemas.Base import Base


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    address_id: Mapped[UUID] = mapped_column(ForeignKey('addresses.id'), nullable=True)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default='pending')

    user = relationship("User")
    address = relationship("Address")
    products = relationship("Product", secondary="order_products")