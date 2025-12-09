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
    stock_quantity: Mapped[int] = mapped_column(nullable=False)

    def to_dict(self, serialize_complex_types: bool = True):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if serialize_complex_types:
                if isinstance(value, UUID):
                    value = str(value)
            result[c.name] = value
        return result
