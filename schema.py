from pydantic import BaseModel
# Pydantic schema for request validation
class MovieCreate(BaseModel):
    imdbId: str
    title: str
    releaseDate: str = None
    trailerLink: str = None
    genres: list[str] = []
    poster: str = None
    backdrops: list[str] = []

class ReviewCreate(BaseModel):
    userId: str
    body: str
    imdbId: str  

class UserCreate(BaseModel):
    name: str
    email: str
    password: str