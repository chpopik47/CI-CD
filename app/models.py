from sqlalchemy import String, Integer, Boolean, ForeignKey, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    specialty: Mapped[str] = mapped_column(String(120))

    slots: Mapped[list["Slot"]] = relationship(back_populates="doctor")


class Slot(Base):
    __tablename__ = "slots"
    __table_args__ = (UniqueConstraint("doctor_id", "date", "time", name="uq_slot"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    date: Mapped[str] = mapped_column(String(10))   # keep simple: YYYY-MM-DD
    time: Mapped[str] = mapped_column(String(5))    # HH:MM
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    doctor: Mapped["Doctor"] = relationship(back_populates="slots")
