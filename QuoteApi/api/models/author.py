from api import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class AuthorModel(db.Model):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=False)
    surname: Mapped[str] = mapped_column(String(32), server_default="Unknown", index=True, unique=False)
    quotes: Mapped[list['QuoteModel']] = relationship(back_populates='author', lazy='dynamic')

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
    def to_dict(self):
        return {"id": self.id, "name": self.name, "surname": self.surname  }