from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from sqlalchemy import String
class Contacts(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    country_code: Mapped[str] = mapped_column(String(5), nullable=True)
    phn_num: Mapped[str] = mapped_column(String(20))
    normalised_num : Mapped[str] = mapped_column(String(20), default="Not Available")
    email: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    last_modified: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)