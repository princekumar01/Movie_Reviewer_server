from fastapi import APIRouter, HTTPException, Depends
from models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database import get_db
from schema import UserCreate
import bcrypt
router = APIRouter(tags=["users"])



@router.post("/watchlist/{user_id}/{imdbId}", status_code=201)
def add_to_watchlist(user_id:str,imdbId:str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userId == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if imdbId not in db_user.watchList:
        db_user.watchList.append(imdbId)
        db.commit()
    return {"detail": "Movie added to watchlist", "imdbId": imdbId}

@router.delete("/watchlist/{user_id}/{imdbId}")
def remove_from_watchlist(user_id: str, imdbId: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.userId == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if imdbId in db_user.watchList:
        db_user.watchList.remove(imdbId)
        db.commit()
    return {"detail": "Movie removed from watchlist", "imdbId": imdbId}



@router.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    # Generate userId from email
    user_id = user.email.split('@')[0]
    # Create the user instance
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        userId=user_id,
        watchlist=[]
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # You can generate a JWT token here if needed, for now just return success
        return db_user
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))
    

@router.post("/login")
def login_user(request: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    is_auth = bcrypt.checkpw(request.password.encode('utf-8'), db_user.password.encode('utf-8'))
    if not is_auth:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # You can generate and return a JWT token here if needed
    return {"detail": "Login successful", "userId": db_user.userId}