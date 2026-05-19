from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
        )
    email: Mapped[str] = mapped_column(
        unique=True, index=True
    )
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)

    tasks: Mapped[list["Task"]]= relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )