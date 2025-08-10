from fastapi import APIRouter, HTTPException, Depends, Request
from models import Movie
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database import get_db
from schema import MovieCreate

router = APIRouter(tags=["movies"])


@router.get("/",response_model=list[MovieCreate],status_code=200)
def get_all(request: Request, db: Session = Depends(get_db)):
    movies = db.query(Movie) .all()
    return movies

@router.get("/movies/{movie_id}", response_model=MovieCreate, status_code=200)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/movies",status_code=201)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(
        imdbId=movie.imdbId,
        title=movie.title,
        releaseDate=movie.releaseDate,
        trailerLink=movie.trailerLink,
        genres=movie.genres,
        poster=movie.poster,
        backdrops=movie.backdrops,
    )
    try:
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

@router.put("/movies/{movie_id}", response_model=MovieCreate)
def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    return {"detail": "Movie deleted successfully"}

