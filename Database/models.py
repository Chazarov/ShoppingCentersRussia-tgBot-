from sqlalchemy import String, Text, DateTime, func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata_obj = MetaData()

class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default = func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default = func.now())

class ShoppingCenter(Base):
    __tablename__ = 'shopping_center'
    id: Mapped[str] = mapped_column(String(10), primary_key = True)
    city: Mapped[str] = mapped_column(String(150), nullable = False)
    name: Mapped[str] = mapped_column(String(150), nullable = False)
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(Text)
    contacts: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(String(150))


