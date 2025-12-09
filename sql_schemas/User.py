from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from uuid import UUID, uuid4

from sql_schemas.Base import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=True,
        onupdate=datetime.now
    )

    addresses = relationship("Address", back_populates="user")

    def to_dict(self, serialize_complex_types: bool = True):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)

            if serialize_complex_types:
                if isinstance(value, UUID):
                    value = str(value)
                elif isinstance(value, datetime):
                    value = value.isoformat()
                elif hasattr(value, 'isoformat'):
                    value = value.isoformat()

            result[c.name] = value
        return result