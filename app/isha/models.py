from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Sutra(Base):
    __tablename__ = "isha_sutras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[int] = mapped_column(Integer, unique=True)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)

    transliterations: Mapped[list["Transliteration"]] = relationship(
        "Transliteration", back_populates="sutra", cascade="all, delete-orphan"
    )
    meanings: Mapped[list["Meaning"]] = relationship(
        "Meaning", back_populates="sutra", cascade="all, delete-orphan"
    )
    interpretations: Mapped[list["Interpretation"]] = relationship(
        "Interpretation", back_populates="sutra", cascade="all, delete-orphan"
    )
    audios: Mapped[list["Audio"]] = relationship(
        "Audio", back_populates="sutra", cascade="all, delete-orphan"
    )
    bhashyams: Mapped[list["Bhashyam"]] = relationship(
        "Bhashyam", back_populates="sutra", cascade="all, delete-orphan"
    )


class Transliteration(Base):
    __tablename__ = "isha_transliterations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    sutra_id: Mapped[int] = mapped_column(
        ForeignKey("isha_sutras.id", ondelete="CASCADE")
    )

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="transliterations")


class Meaning(Base):
    __tablename__ = "isha_meanings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    sutra_id: Mapped[int] = mapped_column(
        ForeignKey("isha_sutras.id", ondelete="CASCADE")
    )

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="meanings")


class Interpretation(Base):
    __tablename__ = "isha_interpretations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    philosophy: Mapped[str] = mapped_column(String(50), nullable=False)
    sutra_id: Mapped[int] = mapped_column(
        ForeignKey("isha_sutras.id", ondelete="CASCADE")
    )

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="interpretations")




class Audio(Base):
    __tablename__ = "isha_audio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    file_path: Mapped[str] = mapped_column(String(500))  # Relative to static directory
    mode: Mapped[str] = mapped_column(String(10))
    sutra_id: Mapped[int] = mapped_column(
        ForeignKey("isha_sutras.id", ondelete="CASCADE")
    )

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="audios")



class Bhashyam(Base):
    __tablename__ = "isha_bhashyams"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sutra_id: Mapped[int] = mapped_column(Integer, ForeignKey("isha_sutras.id", ondelete="CASCADE"))
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    philosophy: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="bhashyams")



# class Bhashyam(Base):
#     __tablename__ = "isha_bhashyams"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     language: Mapped[str] = mapped_column(String(50), nullable=False)
#     text: Mapped[str] = mapped_column(Text, nullable=False)
#     philosophy: Mapped[str] = mapped_column(String(50), nullable=False)  
#     sutra_id: Mapped[int] = mapped_column(
#         ForeignKey("isha_sutras.id", ondelete="CASCADE")
#     )           

#     sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="bhashyam")
