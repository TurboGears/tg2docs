"""The Movie database class"""

from sqlalchemy import Column
from sqlalchemy.types import Date, Integer, String, Text

from toscasample.model import DeclarativeBase


class Movie(DeclarativeBase):

    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)
    genre = Column(Integer, nullable=True)
    release_date = Column(Date, nullable=True)

    def __str__(self):
        if self.year:
            return '"%s" (%d)' % (self.title, self.year)
        else:
            return '"%s"' % self.title
