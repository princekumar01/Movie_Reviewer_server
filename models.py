from sqlalchemy import Column, Integer, String, ARRAY
from database import Base
import re
from sqlalchemy.orm import validates

class  Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    imdbId = Column(String, unique=True,nullable=False)
    title = Column(String, nullable=False)
    releaseDate = Column(String)
    trailerLink = Column(String)
    genres = Column(ARRAY(String))
    poster = Column(String)
    backdrops = Column(ARRAY(String))

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)
    imdbId = Column(String, nullable=False)
    userId = Column(String, nullable=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    watchList = Column(ARRAY(String))
    userId = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Keep only one password column
   
    

    @validates('email')
    def validate_email(self, key, address):
        if not re.match(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$', address):
            raise ValueError(f"{address} is not a valid email!")
        return address

    @validates('password')
    def validate_password(self, key, password):
        if len(password) <= 6:
            raise ValueError("Password must be greater than 6 characters!")
        return password