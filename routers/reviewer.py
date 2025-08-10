from fastapi import APIRouter, HTTPException, Depends
from models import Review
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database import get_db
from schema import ReviewCreate

router = APIRouter(tags=["reviews"])



@router.post("/reviews", status_code=201)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(
        userId=review.userId,
        imdbId=review.imdbId,
        body=review.body
    )
    try:
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(err))

@router.put("/reviews/{review_id}", response_model=ReviewCreate)
def update_review(review_id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    db_review.body = review.body
    db.commit()
    db.refresh(db_review)
    return db_review

@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return {"detail": "Review deleted successfully"}
