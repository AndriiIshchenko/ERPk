import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    deactivated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="product"
    )
    history: Mapped[list["ProductHistory"]] = relationship(
        "ProductHistory", back_populates="product", order_by="ProductHistory.changed_at.desc()"
    )

    @property
    def is_active(self) -> bool:
        return self.deactivated_at is None
