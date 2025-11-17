from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from sql_schemas.Base import Base


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
